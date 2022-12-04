import pandas as pd
import numpy as np
from lux.core.series import LuxSeries
import time

class ExecutorOptimizer:

    def __init__(self):
        self.single_groupby_active = True
        self.hierarchical_count_groupby_active = True
        self.heatmap_2d_groupby_active = True
        self.bin_active = True

        # Cache optimization
        self._cache = {}
        self.hits = {
            "histogram": 0,
            "cut": 0
        }
        self.total_access = {
            "histogram": 0,
            "cut": 0
        }

        # Single groupby optimization
        self._single_groupby_cache = {}
        self._executed_single_groupbys = {}

        # Multi groupby optimization
        self.hierarchical_count_groupby_K = 3
        self.hierarchical_count_groupby_max_arity = 10
        self._hierarchical_count_groupby_attrs = []
        self._executed_hierarchical_count_groupbys = {}

        # Heatmap groupby caching
        self.heatmap_2d_groupby_K = 100
        self._heatmap_2d_groupby_attrs = {}
        self._heatmap_2d_groupby_results = {}
        

    def cut(self, x, bins):
        if not self.bin_active:
            return pd.cut(x, bins)

        hash = pd.util.hash_pandas_object(x).values.tobytes()
        key = ("cut", hash, bins)
        self.total_access["cut"] += 1
        if key in self._cache:
            self.hits["cut"] += 1
            return self._cache[key]
        res = pd.cut(x, bins)
        self._cache[key] = res
        return res

    def histogram(self, series: LuxSeries, bins=10):
        if not self.bin_active:
            return np.histogram(series, bins=bins)

        hash = pd.util.hash_pandas_object(series).values.tobytes()
        key = ("histogram", hash, bins)
        self.total_access["histogram"] += 1
        if key in self._cache:
            self.hits["histogram"] += 1
            return self._cache[key]
        res = np.histogram(series, bins=bins)
        self._cache[key] = res
        return res

    def add_potentially_relevant_single_groupby(self, attr, agg_func, vis):
        if attr not in self._single_groupby_cache:
            self._single_groupby_cache[attr] = [(vis, agg_func)]
        self._single_groupby_cache[attr].append((vis, agg_func))

    def execute_single_groupbys(self):
        if not self.single_groupby_active:
            return
        # attr = group by attribute
        for attr, agg_funcs_info in self._single_groupby_cache.items():
            # Invariants:
            # 1. The same column name across multiple vis tables has the same data but maybe not the same agg function (?)
            # 2. The vis data table for every inputted vis should be the same.

            # Apply agg functions to the columns (ensure the same column only ever has one agg applied to it) and then filter out irrelevant columns when retrieving

            union = agg_funcs_info[0][0].data

            # THIS IS COPIED (in a slightly modified form) FROM PANDAS EXECUTOR
            attrs = set([])
            for vis, _ in agg_funcs_info:
                for clause in vis._inferred_intent:
                    if clause.attribute != "Record":
                        attrs.add(clause.attribute)
            union = union[list(attrs)]

            groupby_result = union.groupby(attr, dropna=False, history=False)
            funcs = set([info[1] for info in agg_funcs_info])

            for func in funcs:
                # TODO: This is inefficient as we will compute aggs for unneeded columns
                agg = groupby_result.agg(func).reset_index()
                self._executed_single_groupbys[(attr, func)] = agg

    def retrieve_executed_single_groupby(self, attr, agg_func, vis):
        if not self.single_groupby_active:
            return None

        key = (attr, agg_func)
        if key not in self._executed_single_groupbys:
            return None

        # THIS IS COPIED FROM PANDAS EXECUTOR
        attributes = set([])
        for clause in vis._inferred_intent:
            if clause.attribute != "Record":
                attributes.add(clause.attribute)

        agg = self._executed_single_groupbys[key][list(attributes)]
        return agg

    # These are only for COUNTs
    def add_relevant_hierarchical_count_groupby(self, attr, vis) -> bool:
        if attr in vis._vis_data.cardinality and vis._vis_data.cardinality[attr] <= self.hierarchical_count_groupby_max_arity:
            self._hierarchical_count_groupby_attrs.append((attr, vis))
            return True
        return False

    def execute_hierarchical_count_groupbys(self):
        if not self.hierarchical_count_groupby_active:
            return
        batch = []
        attributes = set([])
        for i, (attr, vis) in enumerate(self._hierarchical_count_groupby_attrs):
            batch.append(attr)
            for clause in vis._inferred_intent:
                if clause.attribute != "Record":
                    attributes.add(clause.attribute)

            if len(batch) == self.hierarchical_count_groupby_K or i == len(self._hierarchical_count_groupby_attrs) - 1:
                # Copied from execute_aggregate
                # TODO: possible opt: give batch an ID and then map result of groupby to batch
                index_name = vis.data.index.name
                if index_name == None:
                    index_name = "index"

                # batch_col_name = "batch_col_INTERNAL_ONLY"
                # vis._vis_data[batch_col_name] = vis.data[list(attributes)].apply(lambda row: str(row), axis=1)
                # vis._vis_data[batch_col_name] = vis.data[batch].apply(lambda x: pd.factorize(x)[0], axis=1)
                
                #**{batch_col_name: vis.data[batch].agg("-".join, axis=1)})
                # pre_group = vis._vis_data

                # THIS IS COPIED FROM PANDAS EXECUTOR
                # print("pre group:", pre_group[batch_col_name])

                start_time = time.time()
                # first_pass = pre_group.groupby("batch_col_INTERNAL_ONLY", dropna=False, history=False).size().rename("Record").reset_index()
                first_pass = vis._vis_data.groupby(batch, dropna=False, history=False).size().rename("Record")
                # print(f"First pass time [{batch}]: {time.time() - start_time}")
                for attr in batch:
                    self._executed_hierarchical_count_groupbys[attr] = first_pass

                batch.clear()
                attributes.clear()

    def retrieve_executed_hierarchical_count_groupby(self, attr, vis):
        if not self.hierarchical_count_groupby_active or attr not in self._executed_hierarchical_count_groupbys:
            return None
        first_pass = self._executed_hierarchical_count_groupbys[attr]

        # Copied from execute_aggregate
        index_name = vis.data.index.name
        if index_name == None:
            index_name = "index"

        # THIS IS COPIED FROM PANDAS EXECUTOR
        attributes = set([])
        for clause in vis._inferred_intent:
            if clause.attribute != "Record":
                attributes.add(clause.attribute)

        agg = first_pass.groupby(attr, dropna=False, history=False).sum().reset_index().rename({index_name: "Record"})

        return agg

    def add_relevant_heatmap_2d_groupby(self, x_attr, y_attr, vis):
        if x_attr not in self._heatmap_2d_groupby_attrs:
            self._heatmap_2d_groupby_attrs[x_attr] = set()
        self._heatmap_2d_groupby_attrs[x_attr].add((y_attr, vis))

    def execute_heatmap_2d_groupbys(self, bin_size):
        if not self.heatmap_2d_groupby_active:
            return
        for x_attr, y_attr_set in self._heatmap_2d_groupby_attrs.items():
            if len(y_attr_set) <= 3: # 3 is chosen as a middle ground, can eb tuned
                continue # This optimization hurts we can't group by many attrs
            batch = set()
            data = pd.DataFrame()
            for i, (y_attr, vis) in enumerate(y_attr_set):
                batch.add(y_attr)
                data[y_attr] = self.cut(vis._vis_data[y_attr], bin_size)

                # color_attr = vis.get_attr_by_channel("color")
                # if len(color_attr) > 0:
                #     data[color_attr[0].attribute] = vis._vis_data[color_attr[0].attribute]

                if i != 0 and i % self.heatmap_2d_groupby_K == 0 or i == len(y_attr_set) - 1:
                    data[x_attr] = self.cut(vis._vis_data[x_attr], bin_size)
                    batch.add(x_attr)
                    first_pass = data.groupby(list(batch), history=False, observed=True).size().reset_index()
                    for batch_attr in batch:
                        self._heatmap_2d_groupby_results[(x_attr, batch_attr)] = first_pass
                    data = pd.DataFrame()
                    batch.clear()

    def retrieve_executed_heatmap_2d_groupbys(self, x_attr, y_attr, vis):
        if not self.heatmap_2d_groupby_active or (x_attr, y_attr) not in self._heatmap_2d_groupby_results:
            return None
        first_pass = self._heatmap_2d_groupby_results[(x_attr, y_attr)]
        first_pass["xBin"], first_pass["yBin"] = first_pass[x_attr], first_pass[y_attr]
        result = first_pass.groupby(["xBin", "yBin"], history=False)
        return result

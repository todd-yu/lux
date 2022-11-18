import pandas as pd
import numpy as np
from lux.vis.VisList import VisList
from lux.vis.Vis import Vis
from lux.core.frame import LuxDataFrame
from lux.core.series import LuxSeries
from lux.executor.Executor import Executor
import time

class ExecutorOptimizer:
    def __init__(self):
        self._cache = {}

        self.hits = {
            "histogram": 0,
            "cut": 0
        }
        self.total_access = {
            "histogram": 0,
            "cut": 0
        }

        self._single_groupby_cache = {}
        self._executed_single_groupbys = {}

    def cut(self, x, bins):
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
        # TODO: Ensure that vis titles are unique
        for attr, agg_funcs_info in self._single_groupby_cache.items():
            # Invariants:
            # 1. Vis tables for single group bys have two columns: the group by attr and the col to agg
            # 2. The agg function may or may not be the same for every vis
            # 3. The same column name across multiple vis tables has the same data but maybe not the same agg function (?)
            # 4. If the same agg function was used on the same column, then a simple union works

            # Union all the vis data tables together, apply agg functions to the columns (ensure the same column only ever has one agg applied to it) and then filter out irrelevant columns when retrieving

            #union = pd.concat([info[0].data for info in agg_funcs_info])
            union = agg_funcs_info[0][0].data
            # for i in range(1, len(agg_funcs_info)):
            #     union = pd.concat(union, (agg_funcs_info[i][0].data))

            groupby_result = union.groupby(attr, dropna=False, history=False)
            funcs = set([info[1] for info in agg_funcs_info])
            if len(funcs) != 1:
                # TODO: Support multiple agg funcs
                continue
            
            groupby_result = groupby_result.agg(list(funcs)[0]).reset_index()

            # print(groupby_result)
            for (vis, agg_func) in agg_funcs_info:
                # groupby_result = vis.data.groupby(attr, dropna=False, history=False)
                # self._executed_single_groupbys[(attr, agg_func)] = groupby_result.agg(agg_func)
                self._executed_single_groupbys[(attr, agg_func)] = groupby_result

    def retrieve_executed_single_groupby(self, attr, agg_func, vis):
        key = (attr, agg_func)
        if key not in self._executed_single_groupbys:
            return None

        # groupby_result = vis.data.groupby(attr, dropna=False, history=False)
        # self._executed_single_groupbys[(attr, agg_func)] = groupby_result.agg(agg_func)
        
        # print(vis.data.columns)
        # print(self._executed_single_groupbys[key].columns)

        # TODO: THIS IS COPIED FROM PANDAS EXECUTOR
        attributes = set([])
        for clause in vis._inferred_intent:
            if clause.attribute != "Record":
                attributes.add(clause.attribute)

        agg = self._executed_single_groupbys[key][list(attributes)]
        return agg
        # return agg[attr, vis.title]
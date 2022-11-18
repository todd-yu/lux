import pandas as pd
import numpy as np
from lux.core.series import LuxSeries

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
        self.active = True

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
        if not self.active:
            return
        # attr = group by attribute
        for attr, agg_funcs_info in self._single_groupby_cache.items():
            # Invariants:
            # 1. The same column name across multiple vis tables has the same data but maybe not the same agg function (?)
            # 2. The vis data table for every inputted vis should be the same.

            # Apply agg functions to the columns (ensure the same column only ever has one agg applied to it) and then filter out irrelevant columns when retrieving

            union = agg_funcs_info[0][0].data

            groupby_result = union.groupby(attr, dropna=False, history=False)
            funcs = set([info[1] for info in agg_funcs_info])

            for func in funcs:
                # TODO: This is inefficient as we will compute aggs for unneeded columns
                agg = groupby_result.agg(func).reset_index()
                self._executed_single_groupbys[(attr, func)] = agg

    def retrieve_executed_single_groupby(self, attr, agg_func, vis):
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

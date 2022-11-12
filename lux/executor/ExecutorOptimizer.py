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

    @staticmethod
    def batchgroupby():
        pass
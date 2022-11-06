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
        self.hits = 0
        self.total_access = 0

    def cut(self, x, bins):
        hash = np.sum(pd.util.hash_pandas_object(x))
        # TODO: Hash x instead of vis data
        key = ("cut", hash, bins)
        self.total_access += 1
        if key in self._cache:
            self.hits += 1
            return self._cache[key]
        start = time.time()
        res = pd.cut(x, bins)
        print("cut", time.time() - start)
        self._cache[key] = res
        return res

    def histogram(self, series: LuxSeries, bins=10):
        # hash = np.sum(pd.util.hash_pandas_object(series))
        # key = ("histogram", hash, bins)
        # self.total_access += 1
        # if key in self._cache:
        #     self.hits += 1
        #     return self._cache[key]
        res = np.histogram(series, bins=bins)
        # self._cache[key] = res
        return res

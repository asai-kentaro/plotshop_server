import sys
import contextlib
import json
from io import TextIOWrapper, StringIO
import numpy as np
import pandas as pd

from dataman.models import File, DataChank

#
# code executor for breakout mode
# - Code execution is halted at each breakpoint.
#
class CodeExecutorBreakout:
    _unique_instance = None

    breakout_idx = None
    breakout_codes = []
    env_l = {}
    out_var = {}
    env_g = {}

    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            cls._unique_instance = cls()
        return cls._unique_instance

    def __init__(self):
        self.breakout_idx = 0
        self.breakout_codes = []
        def ___setOutputTargetVar(key):
            df = self.env_l[key]
            self.out_var[key] = {
                "head": df.columns,
                "data": df.values,
            }
        def ___clearDataChank(key):
            try:
                dc = DataChank.objects.get(name=key + "_dc").delete()
            except:
                pass
        def ___loadDataChank(key):
            try:
                dc = DataChank.objects.get(name=key + "_dc")
            except:
                return
            dc.data = dc.data.replace("'", '"')
            jsonData = json.loads(dc.data)
            self.env_l[key] = pd.DataFrame(jsonData['data'])
            self.env_l[key].columns = jsonData['head']
        self.env_g = {
            "___setOutputTargetVar": ___setOutputTargetVar,
            "___loadDataChank": ___loadDataChank,
            "___clearDataChank": ___clearDataChank,
        }
        self.env_l = {}
        self.out_var = {}

    def set_breakout_code(self, codes):
        self.breakout_codes = codes
        self.breakout_idx = 0
        self.env_l = {}
        self.out_var = {}

    def get_next_exec_breakout_code(self):
        if self.breakout_idx >= len(self.breakout_codes):
            return
        code = self.breakout_codes[self.breakout_idx]
        self.breakout_idx += 1
        return code

    def progress_breakout_code(self):
        if self.breakout_idx >= len(self.breakout_codes):
            return

        code = self.get_next_exec_breakout_code()

        def jsonizer(obj):
            if isinstance(obj, list):
                #print("-list")
                for i in range(len(obj)):
                    obj[i] = jsonizer(obj[i])
                return obj
            elif isinstance(obj, dict):
                #print("-dict")
                for k, v in obj.items():
                    obj[k] = jsonizer(v)
                return obj
            else:
                if obj.__class__ == np.ndarray:
                    #print("-NP")
                    return obj.tolist()
                elif obj.__class__ == pd.Series:
                    #print("-SR")
                    return obj.as_matrix().tolist()
                elif obj.__class__ == pd.DataFrame:
                    return obj.as_matrix().tolist()
                elif obj.__class__ == pd.Index:
                    return obj.tolist()
                else:
                    return obj

        @contextlib.contextmanager
        def stdoutIO(stdout=None):
            old = sys.stdout
            if stdout is None:
                stdout = StringIO()
            sys.stdout = stdout
            yield stdout
            sys.stdout = old
        with stdoutIO() as s:
            exec(code, self.env_g, self.env_l)
        json_res = {}
        for k, v in self.out_var.items():
            try:
                v = jsonizer(v)
                json.dumps(v)
                json_res[k] = v
            except:
                print("[error] jsoninzer")
                pass

        if self.breakout_idx >= len(self.breakout_codes):
            res = {
                "status": "executed_ended",
                "res": {
                    "index": self.breakout_idx,
                    "max": len(self.breakout_codes),
                },
            }
            return res

        res = {
            "status": "executed",
            "res": {
                "val": s.getvalue(),
                "out_vars": json_res,
                "breakout": {
                    "index": self.breakout_idx,
                    "max": len(self.breakout_codes),
                },
            },
        }
        return res

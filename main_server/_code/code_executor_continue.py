import sys
import contextlib
import json
from io import TextIOWrapper, StringIO
import numpy as np
import pandas as pd

from dataman.models import File, DataChank

#
# code executor for continue mode
# - Code is continuously executed.
#
class CodeExecutorContinue:
    _unique_instance = None

    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            cls._unique_instance = cls()
        return cls._unique_instance

    def exec_code(self, codes):
        out_var = {}
        env_l = {}
        env_g = {}

        def ___setOutputTargetVar(key):
            df = env_l[key]
            out_var[key] = {
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
            env_l[key] = pd.DataFrame(jsonData['data'])
            env_l[key].columns = jsonData['head']

        env_g = {
            "___setOutputTargetVar": ___setOutputTargetVar,
            "___loadDataChank": ___loadDataChank,
            "___clearDataChank": ___clearDataChank,
        }

        # jsonize return value (e.g. np.array to list)
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
            for code in codes:
                exec(code, env_g, env_l)

        json_res = {}
        for k, v in out_var.items():
            try:
                v = jsonizer(v)
                json.dumps(v)
                json_res[k] = v
            except:
                print("[error] jsoninzer")
                pass
        res = {
            "status": "executed",
            "res": { "val": s.getvalue(), "out_vars": json_res },
        }
        return res

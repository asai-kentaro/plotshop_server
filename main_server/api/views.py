import subprocess
import sys
import contextlib
import json
import csv
from io import StringIO
import numpy as np
import pandas as pd
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from codeman.models import CodeElement, CodeMeta
from dataman.models import File, DataChank
from _code.code_executor import CodeExecutor

code_executor = CodeExecutor.get_instance()

@csrf_exempt
def do_exec_local(request):
    def printStderr(msg):
        sys.stderr.write(msg)

    if(request.method == 'POST'):
        data = JSONParser().parse(request)
        out_var = {}
        env_l = {}

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
        codes = data['codes']

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
            codes = data['codes']
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
        resp = {
            "response": res,
            "error": "",
        }
        return JsonResponse(resp)

    print("[Error]")
    res = {
        "status": "error",
        "value": "request get not permitted",
    }
    return JsonResponse(res)

@csrf_exempt
def exec_code_with_breakout(request):
    if(request.method == 'POST'):
        data = JSONParser().parse(request)
        type = data["type"]
        if type == "code_set":
            res = code_executor.set_breakout_code(data["codes"])
            resp = {
                "response": res,
                "error": "",
            }
        if type == "progress_breakout":
            res = code_executor.progress_breakout_code()
            resp = {
                "response": res,
                "error": "",
            }

        return JsonResponse(resp)

    print("[Error]")
    res = {
        "status": "error",
        "value": "request get not permitted",
    }
    return JsonResponse(res)

def load_code(request, code_id):
    codeelm = CodeElement.objects.get(id=code_id)
    res = {
        "code_id": code_id,
        "code": codeelm.code,
    }
    return JsonResponse(res)

def load_csv(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        filedir = "./mysite/uploads/" + data["filename"]
        import csv

        csv_file = open(filedir, "r", encoding="utf-8", errors="", newline="" )
        #リスト形式
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

        res = []
        for row in f:
            res.append(row)

        res = {
            "status": "success",
            "data": res,
        }
        return JsonResponse(res)

    res = {
        "status": "error",
        "value": "request get not permitted",
    }
    return JsonResponse(res)

def post_meta(request, code_id):
    if(request.method == 'POST'):
        #data = json.loads(request.body)


        codeMeta = CodeMeta()
        codeMeta.code = CodeElement.objects.get(id=code_id)
        codeMeta.meta = request.body.decode('utf-8')
        try:
            prev_cm = CodeMeta.objects.get(code=codeMeta.code)
            prev_cm.delete()
            codeMeta.save()
        except CodeMeta.DoesNotExist:
            codeMeta.save()

        res = {
            "status": "success",
            "data": code_id,
        }
        return JsonResponse(res)
    else:
        code = CodeElement.objects.get(id=code_id)
        codeMeta = CodeMeta.objects.get(code=code)

        res = {
            "status": "success",
            "data": codeMeta.meta,
        }
        return JsonResponse(res)

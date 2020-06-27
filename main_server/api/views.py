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
from _code.code_executor_breakout import CodeExecutorBreakout
from _code.code_executor_continue import CodeExecutorContinue

code_executor_breakout = CodeExecutorBreakout.get_instance()
code_executor_continue = CodeExecutorContinue.get_instance()

@csrf_exempt
def exec_code_with_continue(request):
    if(request.method == 'POST'):
        data = JSONParser().parse(request)
        codes = data["codes"]
        res = code_executor_continue.exec_code(codes)
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
            res = code_executor_breakout.set_breakout_code(data["codes"])
            resp = {
                "response": res,
                "error": "",
            }
        if type == "progress_breakout":
            res = code_executor_breakout.progress_breakout_code()
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

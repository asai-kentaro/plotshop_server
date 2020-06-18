from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from basic.models import Entry
from basic.serializer import EntrySerializer
import urllib.request, json

@csrf_exempt
def execution(request):
    if(request.method == 'POST'):
        data = JSONParser().parse(request)
        code_id = data['code_id']

        codes = Entry.objects.filter(code_id=code_id, status='pending')
        if(codes.count()==0):
            return JsonResponse({'res': 'fail'})

        codeelm = codes[0]
        env_g = {}
        env_l = {}
        res = exec(codeelm.code, env_g, env_l)
        obj = {
            "code_id": code_id,
            "res": res,
            "env_l": env_l,
        }
        codeelm.status = "executed"
        codeelm.save()

        return JsonResponse(obj)

    return JsonResponse("{}")

@api_view(['GET'])
def entry_list(request, code_id):
    entries = Entry.objects.filter(code_id=code_id).all()
    serial = EntrySerializer(entries, many=True)
    return Response(serial.data)

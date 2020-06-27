from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from django.views.decorators.csrf import csrf_exempt

from .models import File, DataChank
from codeman.models import CodeElement

def dataupload(request):
    data = {
        'remark': request.POST['remark'],
        'file': request.FILES['file'],
    }

    file_serializer = FileSerializer(data=data)
    if file_serializer.is_valid():
        file = file_serializer.save()

        return JsonResponse({"res": "success"})
    else:
        return JsonResponse({"res": "fail"})

def dataupdate(request):
    req = JSONParser().parse(request)
    data = {
        'name': req['filename'],
        'data': req['data'],
    }
    if('version' in req):
        data['version'] = req['version']
        dc = DataChank(**data)
        dc.save()
    else:
        try:
            dc = DataChank.objects.get(name=data['name'])
            dc.version = str(float(dc.version) + 0.1)
            dc.data = data['data']
            dc.save()
        except DataChank.DoesNotExist:
            data['version'] = "1.0"
            dc = DataChank(**data)
            dc.save()

    return JsonResponse({"res": "success"})

def index(request):
    context = {
        "file_list": File.objects.all(),
        "dc_list": DataChank.objects.all(),
    }

    return render(request, 'dataman/index.html', context)

from django.shortcuts import render
from django.http.response import HttpResponse


def enter(request):
    return HttpResponse('Hello World!')

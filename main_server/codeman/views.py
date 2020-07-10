#
# Code management (template code can be saved)
#
from django.shortcuts import render, redirect
from .forms import CodeElementForm
from .models import CodeElement

import urllib.request, json

def index(request):
    codeelm_list = []
    cels = CodeElement.objects.all()
    context = {
        "codeelm_list": cels
    }

    return render(request, 'codeman/code.html', context)

def new(request):
    codeelm_form = CodeElementForm(request.POST or None)
    if(request.method == "POST" and codeelm_form.is_valid()):
        codeelm = codeelm_form.save(commit=False)
        codeelm.save()

        return redirect("codeman:index")

    context = {
        "codeelm_form": codeelm_form,
    }
    return render(request, 'codeman/new.html', context)

def view_code(request, code_id):
    codeelm = CodeElement.objects.get(id=code_id)

    context = {
        "CODE_ID": code_id,
    }
    return render(request, 'index.html', context)

def edit_code(request, code_id):
    codeelm = CodeElement.objects.get(id=code_id)
    codeelm_form = CodeElementForm(request.POST or None, instance=codeelm)
    if(request.method=="POST" and codeelm_form.is_valid()):
        codeelm_new = codeelm_form.save(commit=False)
        codeelm.title = codeelm_new.title
        codeelm.code = codeelm_new.code
        codeelm.save()

        return redirect("codeman:index")

    context = {
        "codeelm_form": codeelm_form
    }
    return render(request, "codeman/new.html", context)

def do_exec_local(request, code_id):
    codeelm = CodeElement.objects.get(id=code_id)

    env_g = {}
    env_l = {}
    res = exec(codeelm.code, env_g, env_l)

    contents = {
        "res": res,
        "env_g": env_g,
        "env_l": env_l,
    }

    return render(request, "codeman/exec_local.html", contents)

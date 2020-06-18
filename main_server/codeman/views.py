from django.shortcuts import render, redirect
from .forms import CodeElementForm
from .models import CodeElement
from dataman.models import FileCodeLink

import urllib.request, json

def get_entries(code_id):
    url = "http://localhost:3000/code/list/" + code_id + "?format=json"
    method = "GET"
    code_request = urllib.request.Request(url, method=method)
    code_response = urllib.request.urlopen(code_request)
    response_body = code_response.read().decode("utf-8")
    entries = json.loads(response_body)
    return entries

def index(request):
    codeelm_list = []
    cels = CodeElement.objects.all()
    for cel in cels:
        id = cel.id
        ary = []
        try:
            fcls = FileCodeLink.objects.filter(code=id).all()
            for fl in fcls:
                ary.append(fl.file.id)
        except Exception:
            pass

        cel.codelinks = ary
        codeelm_list.append(cel)

    context = {
        "codeelm_list": codeelm_list
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

def view(request, code_id):
    codeelm = CodeElement.objects.get(id=code_id)

    try:
        entries = get_entries(code_id)
        context = {
            "codeelm": codeelm,
            "entries": entries
        }
        return render(request, 'codeman/view.html', context)

    except:
        # MLサーバーが起動していない場合
        context = {
            "CODE_ID": code_id,
        }
        return render(request, 'index.html', context)

def edit(request, code_id):
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

def post_exec(request, code_id):
    codeelm = CodeElement.objects.get(id=code_id)

    url = "http://localhost:3000/api/entries/"
    method = "POST"
    headers = {"Content-Type": "application/json"}

    obj = {
        "code_id": code_id,
        "code": codeelm.code,
    }
    json_data = json.dumps(obj).encode("utf-8")

    code_request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(code_request) as code_response:
        response_body = code_response.read().decode("utf-8")


    entries = get_entries(code_id)
    contents = {
        "code_id": code_id,
        "entries": entries,
    }

    return render(request, "codeman/entries.html", contents)

def do_exec(request, code_id):
    codeelm = CodeElement.objects.get(id=code_id)

    url = "http://localhost:3000/code/exec/"
    method = "POST"
    headers = {"Content-Type": "application/json"}

    obj = {
        "code_id": code_id,
        "code": codeelm.code,
    }
    json_data = json.dumps(obj).encode("utf-8")

    code_request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    code_response = urllib.request.urlopen(code_request)
    response_body = code_response.read().decode("utf-8")
    exec_res = json.loads(response_body)

    entries = get_entries(code_id)
    contents = {
        "code_id": code_id,
        "exec_res": exec_res,
        "entries": entries,
    }
    return render(request, "codeman/exec.html", contents)

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

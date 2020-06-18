from django.shortcuts import render

def index(request):
    context = {
        "CODE_ID": "1"
    }
    return render(request, "index.html", context)

from django.shortcuts import render


def home(request):
    text = None
    context = {"text": text}
    return render(request, "pages/home.html", context)


def tos(request):
    text = None
    context = {"text": text}
    return render(request, "pages/tos.html", context)

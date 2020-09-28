"""Pages views to render the home page and terms of service
"""
from django.shortcuts import render


def home(request):
    """Here’s a view that returns the current home page, as an HTML document

    Args:
        request (object): used to generate the response

    Returns:
        object: returns an HttpResponse object with that rendered text
    """
    text = None
    context = {"text": text}
    return render(request, "pages/home.html", context)


def tos(request):
    """Here’s a view that returns the current terms of service, as an HTML document

    Args:
        request (object): used to generate the response

    Returns:
        object: returns an HttpResponse object with that rendered text
    """
    text = None
    context = {"text": text}
    return render(request, "pages/tos.html", context)

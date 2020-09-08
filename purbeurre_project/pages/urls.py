from django.urls import path
from django.views.generic import TemplateView

app_name = "pages"

urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="pages/home.html",
            name="home",
        ),
    ),
    path(
        "",
        TemplateView.as_view(
            template_name="pages/tos.html",
            name="tos",
        ),
    ),
]

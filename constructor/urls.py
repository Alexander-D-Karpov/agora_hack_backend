from django.urls import path

from constructor.api.views import ListCreateFontsApiView

urlpatterns = [
    path("fonts/", ListCreateFontsApiView.as_view(), name="list_create_font_api")
]

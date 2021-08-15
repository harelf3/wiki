from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>",views.get, name = "get"),
    path("wiki/make", views.make, name = "make"),
    path("wiki/random",views.randoms, name ="randoms"),
    
]

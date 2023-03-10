from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("image", views.learn_dance),
    path("dance", views.dance),
]

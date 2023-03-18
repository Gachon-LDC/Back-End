from django.urls import path, include
from . import views
from .controllers import auth
from .controllers.comment import comment_controller


urlpatterns = [
    path("", views.index),
    path("auth", auth.auth_controller),
    path("videos", include("App.controllers.video.url")),
    path("comment", comment_controller),
]

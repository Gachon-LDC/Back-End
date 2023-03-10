from django.urls import path, include
from . import views
from .controllers import auth
from .controllers.comment import comment_controller


urlpatterns = [
    path("", views.index),
    path("image", views.learn_dance),
    path("dance", views.dance),
    path("auth", auth.auth_controller),
    path("video", include("App.controllers.video.url")),
    path("comment", comment_controller),
]

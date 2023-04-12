from django.urls import path, include
from . import views
from .controllers import auth
from .controllers.comment import comment_controller


urlpatterns = [
    path("", views.index),
    path("image", views.learn_dance),
    path("dance", views.dance),
    path("auth", auth.auth_controller),#로그인 엔드포인트
    path("auth/register", auth.auth_register_controller),#회원가입 엔드포인트
    path("videos", include("App.controllers.video.url")),
    path("comment", comment_controller),
]

from django.urls import path, include
from . import views
from .controllers import auth, comment, dance_category


urlpatterns = [
    path("", views.index),
    path("auth", auth.AuthController.as_view()),
    path("auth/register", auth.AuthRegisterController.as_view()),  # 회원가입 엔드포인트
    path("videos", include("App.controllers.video.url")),
    path("comments/<uuid:uid>", comment.CommentItemController.as_view()),  # 코멘트 엔드포인트
    path("danceCategory", dance_category.dance_category_controller),  # 댄스 카테코리 다 가져오기
    path(
        "danceCategory/<uuid:uid>/", dance_category.dance_category_controller_by_videoID
    ),  # 댄스 카테코리 다 가져오기
]

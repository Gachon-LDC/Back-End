from django.urls import path, include
from . import views
from .controllers import auth, comment, dance_category


urlpatterns = [
    path("", views.index),
    path("auth", auth.AuthController.as_view()),
    path("auth/register", auth.AuthRegisterController.as_view()),  # 회원가입 엔드포인트
    path("videos", include("App.controllers.video.url")),
    path("comments/<str:uid>", comment.CommentItemController.as_view()),  # 코멘트 엔드포인트
    path(
        "category", dance_category.DanceCategoryController.as_view()
    ),  # 댄스 카테코리 다 가져오기
    path(
        "category/<str:uid>/", dance_category.DanceCategoryItemController.as_view()
    ),  # 댄스 카테코리 다 가져오기
]

from django.urls import path, include
from . import views
from .controllers import auth,comment,dance_category


urlpatterns = [
    path("", views.index),
    path("image", views.learn_dance),
    path("dance", views.dance),
    path("auth", auth.auth_controller),#로그인 엔드포인트
    path("auth/register", auth.auth_register_controller),#회원가입 엔드포인트
    path("videos", include("App.controllers.video.url")),
    path("comment", comment.comment_controller_byUid),#코멘트 엔드포인트
    path("comment/writerId", comment.comment_controller_byWriterId),#코멘트 작성자 기준 불러오기
    path("comment/videoId", comment.comment_controller_byVideoId),#코멘트 비디오 기준 불러오기
    path("danceCategory", dance_category.dance_category_controller),#댄스 카테코리 다 가져오기
    path("danceCategory/<uuid:uid>/", dance_category.dance_category_controller_by_videoID)#댄스 카테코리 다 가져오기    
]

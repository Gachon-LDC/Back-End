from django.urls import path
from . import (
    VideoController,
    LearnController,
    ContentController,
    CommentController,
)

urlpatterns = [
    path("", VideoController.as_view()),
    path("/<str:video_id>", ContentController.as_view()),
    path("/<str:video_id>/learn", LearnController.as_view()),
    path("/<str:video_id>/comment", CommentController.as_view()),
]

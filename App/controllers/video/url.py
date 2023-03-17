from django.urls import path
from .video import video_controller
from .learn import learn_controller
from .content import content_controller

urlpatterns = [
    path("", video_controller),
    path("/<str:video_id>/", content_controller),
    path("/<str:video_id>/learn/", learn_controller),
]

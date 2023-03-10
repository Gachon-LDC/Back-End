from django.urls import path
from . import video


urlpatterns = [
    path("", video.video_controller),
]

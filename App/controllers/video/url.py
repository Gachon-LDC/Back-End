from django.urls import path
from .video import VideoController
from .learn import learn_controller
from .content import ContentController

urlpatterns = [
    path("", VideoController.as_view()),
    path("/<str:video_id>", ContentController.as_view()),
    path("/<str:video_id>/learn/", learn_controller),
]

from django.http import HttpRequest, JsonResponse
from rest_framework import status
from App.models import VideoModel
from App.serializers import VideoModelSerializer
from App.utils.utils import int_or_0
from App.utils.errors import HttpError
from App.utils.IController import IController
from App.services.video_service import save_video
import uuid


class VideoController(IController):
    """video Controller
    url : /video
    """

    http_method_names = ["get", "post"]

    async def get(self, req: HttpRequest):
        """_summary_ get VideoList
        ### Params
        offset : Optional[int]
        limit : Optional[int]
        """
        offset = int_or_0(req.GET.get("offset"))
        limit = int_or_0(req.GET.get("limit", 10))

        videos = VideoModel.objects.all()[offset:limit]

        serailized = VideoModelSerializer(videos, many=True)
        return JsonResponse(serailized.data, safe=False)

    async def post(req: HttpRequest):
        """
        _summary_ Update Video Info
        Method: POST
        """
        video = VideoModelSerializer(data=req.body)
        if not video.is_valid():
            raise HttpError(status.HTTP_422_UNPROCESSABLE_ENTITY)
        video.uploader_id = uuid.uuid4()
        video.video_id = uuid.uuid4()
        req.FILES.getlist("video")
        saved = await save_video(video)

        return JsonResponse(saved, ensure_ascii=True)

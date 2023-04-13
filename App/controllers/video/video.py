from django.http import HttpRequest, JsonResponse
from rest_framework import status
from App.models import VideoModel
from App.serializers import VideoModelSerializer
from App.utils.utils import int_or_0
from App.utils.errors import HttpError
from App.utils.IController import IController
from App.services.video_service import save_video
from asgiref.sync import sync_to_async
import uuid


class VideoController(IController):
    """video Controller
    url : /video
    """

    http_method_names = ["get", "post"]

    @sync_to_async
    def get(self, req: HttpRequest):
        """_summary_ get VideoList
        ### Params
        offset : Optional[int]
        limit : Optional[int]
        """
        offset = int_or_0(req.GET.get("offset"))
        limit = max([10, int_or_0(req.GET.get("limit", 10))])
        videos = VideoModel.objects.all()[offset : offset + limit]
        serailized = VideoModelSerializer(videos, many=True)
        return JsonResponse(serailized.data, safe=False)

    async def post(self, req: HttpRequest):
        """
        _summary_ Update Video Info
        """
        video = VideoModelSerializer(data={key: req.POST[key] for key in req.POST})
        video_file = req.FILES.get("file")
        if not video.is_valid():
            raise HttpError(status.HTTP_422_UNPROCESSABLE_ENTITY)
        if video_file.content_type != "video/mp4":
            raise HttpError(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        # TODO: get authorized userid
        saved = await save_video(uuid.uuid4(), video, video_file)

        return JsonResponse(saved)

from django.http import HttpRequest, JsonResponse
from rest_framework import status
from App.models import VideoModel
from App.serializers import VideoModelSerializer
from App.utils import int_or_0, IController
from App.utils.errors import HttpError, HTTPStatus
from App.dto.session_user import SessionUser
from App.services import video_service
from asgiref.sync import sync_to_async


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
        _summary_ Upload Video

        req.body : multipart/form-data
        req.FILE["file"] : file - video file

        """
        if (user := SessionUser.from_session(req.session)) is None:
            raise HttpError(HTTPStatus.NOT_FOUND, "로그인이 필요합니다.")
        video = VideoModelSerializer(data={key: req.POST[key] for key in req.POST})
        video_file = req.FILES.get("file")
        if not video.is_valid():
            raise HttpError(status.HTTP_422_UNPROCESSABLE_ENTITY)
        if video_file.content_type != "video/mp4":
            raise HttpError(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        saved = await video_service.save_video(user.uid, video, video_file)

        return JsonResponse(saved)

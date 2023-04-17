from django.http import HttpRequest, JsonResponse, HttpResponse
from App.serializers import VideoModelSerializer, CommentModelSerializer

from App.services import video_service, comment_service
from App.utils import IController
from App.utils.errors import HttpError, HTTPStatus
from App.dto.session_user import SessionUser


class ContentController(IController):
    """_summary_ video_item_controller
    url : /video/[video_id]
    """

    http_method_names = ["get", "post", "delete", "put", "patch"]

    async def get(self, req: HttpRequest, video_id: str):
        """_summary_ GET controller
        return : video information of video id
        """
        ret = await video_service.get_by_id(video_id)
        serialized = VideoModelSerializer(ret)
        ret = serialized.data
        if not req.GET.get("no_comment"):
            comments = await comment_service.get_by_videoId(video_id)
            comment_serialized = CommentModelSerializer(comments, many=True)
            ret["comments"] = comment_serialized.data
        return JsonResponse(ret)

    async def put(self, req: HttpRequest, video_id: str):
        """_summary_ PUT update video"""
        serializer = VideoModelSerializer(req.body)
        serializer.is_valid()

        if (user := SessionUser.from_session(req.session)) is None:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "로그인이 필요합니다.")

        await video_service.update_video(video_id, user.uid, serializer.validated_data)
        return HttpResponse("success")

    async def delete(self, req: HttpRequest, video_id: str):
        """_summary_ DELETE video"""
        if (user := SessionUser.from_session(req.session)) is None:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "로그인이 필요합니다.")
        await video_service.delete_by_id(video_id, user.uid)
        return HttpResponse("success")

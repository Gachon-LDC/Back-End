from django.http import HttpRequest, JsonResponse
from App.utils.errors import HttpError, HTTPStatus
from App.utils import IController
from App.dto.session_user import SessionUser
from App.serializers import CommentModelSerializer
from App.services import comment_service, video_service
from rest_framework.parsers import JSONParser


class CommentController(IController):
    http_method_names = ["get", "post"]

    async def get(self, _: HttpRequest, video_id: str):
        comments = await comment_service.get_by_videoId(video_id)
        serialized = CommentModelSerializer(comments, many=True).data
        return JsonResponse(serialized, status=201)

    async def post(self, req: HttpRequest, video_id: str):
        content = JSONParser().parse(req)["content"]
        print("content", content)
        if content == None:
            raise HttpError(HTTPStatus.BAD_REQUEST, "잘못된 요청입니다.")
        if (user := SessionUser.from_session(req.session)) is None:
            raise HttpError(HTTPStatus.NOT_FOUND, "로그인이 필요합니다.")
        if await video_service.get_by_id(video_id) is None:
            raise HttpError(HTTPStatus.NOT_FOUND, "해당 비디오는 존재하지 않습니다.")
        comment = await comment_service.create(video_id, user.uid, content)
        return JsonResponse(CommentModelSerializer(comment).data, status=201)

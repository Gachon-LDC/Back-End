from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from App.serializers import CommentModelSerializer
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus
from App.services import comment_service
from App.utils import IController
from App.dto.session_user import SessionUser


class CommentItemController(IController):
    """Comment Controller
    url : /comment/[comment_id]
    """

    http_method_names = ["get", "delete", "put"]

    async def get(self, _: HttpRequest, uid: str):
        comment = await comment_service.get_by_uid(uid)
        if comment is None:
            raise HttpError(HTTPStatus.NOT_FOUND, "해당 댓글은 존재하지 않습니다.")
        serializer = CommentModelSerializer(comment)
        return JsonResponse(serializer.data, status=201)

    async def delete(self, req: HttpRequest, uid: str):
        user = SessionUser.from_session(req.session)
        if user is None:
            raise HttpError(HTTPStatus.NOT_FOUND, "로그인이 필요합니다.")
        await comment_service.delete(uid, user.uid)

    async def put(self, req: HttpRequest, uid: str):
        if (user := SessionUser.from_session(req.session)) is None:
            raise HttpError(HTTPStatus.NOT_FOUND, "로그인이 필요합니다.")
        if "content" not in req.data:
            raise HttpError(HTTPStatus.BAD_REQUEST, "잘못된 요청입니다.")
        edited = comment_service.update(uid, req.data["content"], user.uid)
        seralzied = CommentModelSerializer(edited).data
        return JsonResponse(seralzied, status=201)

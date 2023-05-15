from django.http import JsonResponse, HttpResponse, HttpRequest
from App.serializers import CommentModelSerializer
from App.utils.errors import HttpError, HTTPStatus
from App.services import comment_service
from App.utils import IController
from App.dto.session_user import SessionUser
from App.dto.comment_dto import CommentUpdateDTO
import json


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
            raise HttpError(HTTPStatus.UNAUTHORIZED)
        if (comment := await comment_service.get_by_uid(uid)) is None:
            raise HttpError(HTTPStatus.NOT_FOUND)
        await comment_service.delete(comment, user.uid)
        return HttpResponse("success", status=201)

    async def put(self, req: HttpRequest, uid: str):
        if (user := SessionUser.from_session(req.session)) is None:
            raise HttpError(HTTPStatus.UNAUTHORIZED)
        if (comment := await comment_service.get_by_uid(uid)) is None:
            raise HttpError(HTTPStatus.NOT_FOUND)
        data = json.loads(req.body)
        update_dto = CommentUpdateDTO(uid, user.uid, data)
        if update_dto.content is None:
            raise HttpError(HTTPStatus.UNPROCESSABLE_ENTITY)

        edited = comment_service.update(comment, update_dto)
        seralzied = CommentModelSerializer(edited).data
        return JsonResponse(seralzied, status=201)

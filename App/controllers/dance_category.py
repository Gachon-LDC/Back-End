from django.http import JsonResponse, HttpRequest

from App.serializers import DanceCategoryModelSerializer, VideoModelSerializer
from App.services import dance_category_service, video_service
from App.utils import IController
from App.utils.errors import HttpError, HTTPStatus
from App.dto.session_user import SessionUser


class DanceCategoryController(IController):
    http_method_names = ["get", "post"]

    async def get(self, _):
        categories = await dance_category_service.get_all()
        serialized = DanceCategoryModelSerializer(categories, many=True)
        return JsonResponse(serialized.data, status=201, safe=False)

    async def post(self, req: HttpRequest):
        if SessionUser.from_session(req.session) is None:
            raise HttpError(HTTPStatus.UNAUTHORIZED)
        category = await dance_category_service.create(req)
        return JsonResponse(DanceCategoryModelSerializer(category).data, status=201)


class DanceCategoryItemController(IController):
    http_method_names = ["get", "delete", "put"]

    async def get(self, req: HttpRequest, uid: str):
        category = await dance_category_service.get_by_id(uid)
        if category == None:
            raise HttpError(HTTPStatus.NOT_FOUND)
        serialized = DanceCategoryModelSerializer(category).data
        if req.GET.get("video") in ["true", "True"]:
            videos = await video_service.get_by_category(uid)
            video_serialized = VideoModelSerializer(videos, many=True)
            serialized["videos"] = video_serialized.data
        return JsonResponse(serialized, status=201)

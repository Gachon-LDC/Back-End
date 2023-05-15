from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from App.utils.errors import HttpError, HTTPStatus
from App.models import DanceCategoryModel
from App.serializers import DanceCategoryModelSerializer
import uuid


async def get_by_id(uid) -> DanceCategoryModel:
    try:
        row = DanceCategoryModel.objects.get(uid=uid)
        return row
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)


async def get_all():
    try:
        rows = DanceCategoryModel.objects.all()
        return rows
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)


def check_log_in(req: HttpRequest):
    if req.session["user"] != "":
        return True
    else:
        return False


async def create(req: HttpRequest):
    data = JSONParser().parse(req)
    if (title := data.get("title")) is None:
        raise HttpError(HTTPStatus.UNPROCESSABLE_ENTITY)

    newDanceCategoryModel = DanceCategoryModel()
    newDanceCategoryModel.uid = uuid.uuid4()
    newDanceCategoryModel.title = title

    newDanceCategoryModel.save()

    return newDanceCategoryModel

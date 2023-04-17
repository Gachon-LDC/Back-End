from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from App.models import DanceCategoryModel
from App.serializers import DanceCategoryModelSerializer
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus, HttpErrorHandling
from App.services import dance_category_service
from django.contrib.auth.hashers import check_password
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

async def dance_category_controller(req):
    if req.method == "GET":
        return await get_categories(req)
    #댓글을 uid로 찾고 content로 수정함.
    if req.method == "POST":
        if dance_category_service.check_log_in(req):
            return await add_category(req)
        else:
            return HttpResponse("현재 로그인되어 있지 않습니다.",status=404)

    if req.method=="_":
        raise HttpError(HTTPStatus.NOT_FOUND)
    
async def dance_category_controller_by_videoID(req,uid):
    if req.method == "GET":
        return await get_videos_by_category(req,uid)

    if req.method=="_":
        raise HttpError(HTTPStatus.NOT_FOUND)


# GET
async def get_categories(req):
    rows = await dance_category_service.get_all(req)
    
    if(rows==None): return HttpError("카테고리가 존재하지 않습니다.")
    else:
        #serializer = DanceCategoryModelSerializer(rows)
        json_data = serializers.serialize('json', rows)
        print(json_data)
        return HttpResponse(json_data,status=201,content_type = "application/json")


# GET(id)
async def get_videos_by_category(req, uid):
    row = await dance_category_service.get_by_id(uid)
    
    if(row==None): return HttpError("카테고리가 존재하지 않습니다.")
    else:
        #serializer = DanceCategoryModelSerializer(row)
        json_data = serializers.serialize('json', row)
        return HttpResponse(json_data,status=201,content_type = "application/json")


# POST
async def add_category(req):
    return await dance_category_service.dance_category_register(req)

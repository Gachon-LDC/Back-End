from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from App.models import CommentModel
from App.serializers import CommentModelSerializer
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus, HttpErrorHandling
from App.services import auth_service,comment_service
from django.contrib.auth.hashers import check_password
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

@HttpErrorHandling
async def comment_controller_byUid(req):
    if comment_service.check_log_in(req):
        #댓글을 uid로 얻음
        if req.method == "GET":
            data = JSONParser().parse(req)
            uid = data.get("uid")
            return await get_comment_byUid(req, uid)
        #댓글을 uid로 찾고 content로 수정함.
        if req.method == "PUT":
            data = JSONParser().parse(req)
            uid = data.get("uid")
            content = data.get("content")
            return await update_comment_byUid(req,uid,content)
        
        #댓글을 삭제함.
        if req.method == "DELETE":
            data = JSONParser().parse(req)
            uid = data.get("uid")
            return await delete_comment_byUid(req,uid)

        if req.method=="_":
            raise HttpError(HTTPStatus.NOT_FOUND)
    else:
        return HttpResponse("현재 로그인되어 있지 않습니다.",status=404)

@HttpErrorHandling
async def comment_controller_byWriterId(req):
    if comment_service.check_log_in(req):
        #WriterId의 댓글 전체를 얻음
        if req.method == "GET":
            return await get_comment_byWriterId(req)
        
        #WriterId의 댓글 전체를 삭제함.
        if req.method == "DELETE":
            return await delete_comment_byWriterId(req)

        if req.method=="_":
            raise HttpError(HTTPStatus.NOT_FOUND)
    else:
        return HttpResponse("현재 로그인되어 있지 않습니다.",status=404)
    
@HttpErrorHandling
async def comment_controller_byVideoId(req):
    if comment_service.check_log_in(req):
        #VideoId의 댓글 전체를 얻음
        if req.method == "GET":
            data = JSONParser().parse(req)
            videoId = data.get("videoId")
            return await get_comment_byVideoId(req,videoId)
        
        #댓글을 등록함.videoId가 필요
        if req.method == "POST":
            return await create_comment_byVideoId(req)
        
        #VideoId의 댓글 전체를 삭제함
        if req.method == "DELETE":
            data = JSONParser().parse(req)
            videoId = data.get("videoId")
            return await delete_comment_byVideoId(req,videoId)

        if req.method=="_":
            raise HttpError(HTTPStatus.NOT_FOUND)
    else:
        return HttpResponse("현재 로그인되어 있지 않습니다.",status=404)

# GET(id)
# uid에 해당하는 댓글을 리턴함.
async def get_comment_byUid(req:HttpRequest, uid):
    rows = comment_service.check_correct_access(req)
    if rows == False:
        return HttpError("잘못된 유저의 접근입니다.", status = 404)
    else:
        row = rows.filter(uid=uid)
        if(row == None) : return HttpError("해당 댓글은 존재하지 않습니다.")
        serializer = CommentModelSerializer(row)
        
        #result = json.dumps(row,cls=DjangoJSONEncoder)
        return HttpResponse(serializer,status=201,content_type = "application/json")

# update(id):
async def update_comment_byUid(req:HttpRequest, uid,content):
    rows = comment_service.check_correct_access(req)
    if rows == False:
        return HttpError("잘못된 유저의 접근입니다.", status = 404)
    else:
        row = rows.filter(uid=uid)
        if(row == None) : return HttpError("해당 댓글은 존재하지 않습니다.")
        row.content = content
        row.save()
        return HttpError("업데이트 성공했습니다.", status=201)


# DELETE(id)
# uid에 해당하는 댓글을 삭제함.
async def delete_comment_byUid(req:HttpRequest, uid):
    rows = comment_service.check_correct_access(req)
    if rows == False:
        return HttpError("잘못된 유저의 접근입니다.", status = 404)
    else:
        row = rows.filter(uid=uid)
        if(row == None) : return HttpError("해당 댓글은 존재하지 않습니다.")
        row.delete()
        return HttpResponse("삭제에 성공했습니다.",status=201)
    
    
async def get_comment_byWriterId(req:HttpRequest):
    rows=await comment_service.check_correct_access(req)
    if rows==False:
        return HttpResponse("잘못된 유저의 접근입니다.", status = 404)
    else:
        #serializer = CommentModelSerializer(rows)
        json_data = serializers.serialize('json',rows)
        #result = json.dumps(rows,cls=DjangoJSONEncoder)
        return HttpResponse(json_data,status=201,content_type = "application/json")
    
async def delete_comment_byWriterId(req:HttpRequest):
    rows = await comment_service.check_correct_access(req)
    if rows==False:
        return HttpResponse("잘못된 유저의 접근입니다.", status = 404)
    else:
        rows.delete()
        return HttpResponse("삭제에 성공했습니다.", status=201)

#Get()
async def get_comment_byVideoId(req:HttpRequest,videoId):
    rows = await comment_service.get_by_videoId(videoId)
    if rows==False:
        return HttpError("해당 비디오의 코멘트는 존재하지 않습니다.", status = 404)
    else:
        print(rows)
        #serializer = CommentModelSerializer(rows)
        json_data = serializers.serialize('json', rows)
        return HttpResponse(json_data,status=201,content_type = "application/json")

#PUT()
async def create_comment_byVideoId(req:HttpRequest):
    return await comment_service.comment_register(req)

async def delete_comment_byVideoId(req:HttpRequest, videoId):
    rows = await comment_service.get_by_videoId(videoId)
    if rows==False:
        return HttpResponse("해당 비디오의 코멘트는 존재하지 않기에 삭제할 수 없습니다.", status=404)
    else:
        rows.delete()
        return HttpResponse("삭제에 성공했습니다.", status=201)
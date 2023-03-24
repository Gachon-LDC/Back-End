from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from App.models import UserModel
from App.serializers import UserModelSerializer
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus, HttpErrorHandling
from App.services.auth_service import *


@HttpErrorHandling
# 로그인 관련 Controller
def auth_controller(req):
    if req.method == "GET":
        return get_signed_user(req)
        
    # etc...
    #if req.method =="PUT":
    #    return register(req)
    
    if req.method == "POST":
        return sign_in(req)
    
    if req.method == "DELETE":
        return log_out(req)

    if req.method=="_":
        raise HttpError(HTTPStatus.NOT_FOUND)

#회원가입 컨트롤러
def auth_register_controller(req):
    if req.method == "POST":
        return register(req)
    
    if req.method == "DELETE":
        return sign_out(req)
    
    if req.method=="_":
        raise HttpError(HTTPStatus.NOT_FOUND)

# GET User의 정보를 얻음
async def get_signed_user(req:HttpRequest):
    if req.session.get('user',False):
        uid = req.session.get('user',False)
        return get_by_uid(uid)
    else :
        return JsonResponse("현재 로그인되어 있지 않습니다.",status = 404)

# POST 로그인
async def sign_in(req:HttpRequest):
    if await check_user(req):
        await session_save_uid(req)
        
        #여기에 해당 웹 페이지로 이동
        
        #여기서 원하는 페이지로 이동 시킨다.
    else:
        return JsonResponse("일치하는 계정이 없습니다.", status = 404)

#로그 아웃
async def log_out(req:HttpRequest):
    await session_delete_uid(req)
    return JsonResponse("로그아웃 성공", status = 201)
    
# PUT?? 회원 등록#POST로 수정해서 들고오기
async def register(req):
    await user_register(req)
    return JsonResponse("계정 생성 성공", status=201)


# DELETE 회원 탈퇴//로그 아웃
async def sign_out(req):
    return await user_withdraw(req)
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from App.models import UserModel
from App.serializers import UserModelSerializer
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus, HttpErrorHandling
from App.services import auth_service
from django.contrib.auth.hashers import check_password


# 로그인 관련 Controller
@HttpErrorHandling
async def auth_controller(req):
    if req.method == "GET":
        return await get_signed_user(req)
        
    # etc...
    #if req.method =="PUT":
    #    return register(req)
    
    if req.method == "POST":
        return await sign_in(req)
    
    if req.method == "DELETE":
        return await log_out(req)

    if req.method=="_":
        raise HttpError(HTTPStatus.NOT_FOUND)

#회원가입 컨트롤러
@HttpErrorHandling
async def auth_register_controller(req):
    if req.method == "POST":
        return await sign_up(req)
    
    if req.method == "DELETE":
        return await sign_out(req)
    
    if req.method=="_":
        raise HttpError(HTTPStatus.NOT_FOUND)

# GET User의 정보를 얻음
async def get_signed_user(req:HttpRequest):
    if req.session.get('user',False):
        uid = req.session.get('user',False)
        return auth_service.get_by_uid(uid)
    else :
        return HttpResponse("현재 로그인되어 있지 않습니다.",status = 404)

# POST 로그인
async def sign_in(req:HttpRequest):
    data = JSONParser().parse(req)
    user = await auth_service.get_by_email(data.get('email'))
    
    if user==False:
        return HttpResponse("메일과 일치하는 계정이 없습니다.", status = 404)
    
    if check_password(data.get('pwd'), user.pwd):
        auth_service.session_save_uid(req,user)
        return HttpResponse("로그인 성공.",status=201)
        
        #위에거 지우고 여기에 해당 웹 페이지로 이동코드 작성
    else:
        return HttpResponse("비밀번호가 틀렸습니다.", status = 404)

#로그 아웃
async def log_out(req:HttpRequest):
    if req.session['user']!='':
        return HttpResponse("이미 로그아웃 되어 있습니다. 잘못된 접근입니다.",status=404)
    auth_service.session_delete_uid(req)
    return HttpResponse("로그아웃 성공", status = 201)
    
#POST로 수정해서 들고오기
async def sign_up(req):
    return await auth_service.user_register(req)


# DELETE 회원 탈퇴//로그 아웃
async def sign_out(req): 
    if await auth_service.user_withdraw(req):
        return HttpResponse("회원탈퇴성공",status=201)
    else:
        return HttpResponse("회원탈퇴실패",404)
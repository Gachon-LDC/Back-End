from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus, HttpErrorHandling
from App.services import auth_service


# 로그인 관련 Controller
@HttpErrorHandling
async def auth_controller(req):
    if req.method == "GET":
        return await get_signed_user(req)

    # etc...
    # if req.method =="PUT":
    #    return register(req)

    if req.method == "POST":
        return await sign_in(req)

    if req.method == "DELETE":
        return await log_out(req)

    if req.method == "_":
        raise HttpError(HTTPStatus.NOT_FOUND)


# 회원가입 컨트롤러
@HttpErrorHandling
async def auth_register_controller(req):
    if req.method == "POST":
        return await sign_up(req)

    if req.method == "DELETE":
        return await sign_out(req)

    if req.method == "_":
        raise HttpError(HTTPStatus.NOT_FOUND)


# GET User의 정보를 얻음
async def get_signed_user(req: HttpRequest):
    user = auth_service.get_signed_user(req)
    if user is None:
        raise HttpError(HTTPStatus.UNAUTHORIZED, "로그인되어 있지 않습니다.")
    return JsonResponse(user.dict(), status=201)


# POST 로그인
async def sign_in(req: HttpRequest):
    data = JSONParser().parse(req)
    user = await auth_service.get_by_email(data.get("email"))
    if user == False:
        raise HttpError(HTTPStatus.NOT_FOUND, "메일과 일치하는 계정이 없습니다.")

    signed_user = auth_service.sign_in(req, user, data.get("pwd"))
    return JsonResponse(signed_user.dict(), status=201)


# 로그 아웃
async def log_out(req: HttpRequest):
    user = auth_service.get_signed_user(req)
    if user == None:
        return HttpResponse("이미 로그아웃 되어 있습니다. 잘못된 접근입니다.", status=404)
    auth_service.sign_out(req)
    return HttpResponse("로그아웃 성공", status=201)


# POST로 수정해서 들고오기
async def sign_up(req):
    return await auth_service.user_register(req)


# DELETE 회원 탈퇴//로그 아웃
async def sign_out(req):
    if await auth_service.user_withdraw(req):
        return HttpResponse("회원탈퇴성공", status=201)
    else:
        return HttpResponse("회원탈퇴실패", 404)

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus
from App.services import auth_service
from App.utils import IController


# 로그인 관련 Controller
class AuthController(IController):
    """auth controller
    url : /auth
    """

    http_method_names = ["get", "post", "delete"]

    async def get(self, req: HttpRequest):
        """
        get siend user
        return signed user"""
        signed_user = auth_service.get_signed_user(req)
        if signed_user is None:
            raise HttpError(HTTPStatus.NOT_FOUND, "로그인 되어있지 않습니다.")
        return JsonResponse(signed_user.dict())

    async def post(self, req: HttpRequest):
        """sign in"""
        data = JSONParser().parse(req)
        user = await auth_service.get_by_email(data.get("email"))
        if user is None:
            raise HttpError(HTTPStatus.NOT_FOUND, "메일과 일치하는 계정이 없습니다.")

        signed_user = auth_service.sign_in(req, user, data.get("pwd"))
        return JsonResponse(signed_user.dict(), status=201)

    async def delete(self, req: HttpRequest):
        """sign out"""
        if auth_service.get_signed_user(req) is None:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "로그인 되어있지 않습니다.")
        auth_service.sign_out(req.session)
        return HttpResponse("로그아웃 성공", status=201)


class AuthRegisterController(IController):
    """auth register controller
    url : /auth/register
    """

    http_method_names = ["post", "delete"]

    async def post(self, req: HttpRequest):
        """sign up
        register user
        """
        await auth_service.user_register(req)
        return HttpResponse("계정 생성 성공", status=201)

    async def delete(self, req: HttpRequest):
        """sign out
        dereguster user
        """
        session_user = auth_service.get_signed_user(req)
        if session_user is None:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "로그인 되어있지 않습니다.")
        data = JSONParser().parse(req)

        await auth_service.user_withdraw(session_user, data)
        return HttpResponse("회원탈퇴성공", status=201)

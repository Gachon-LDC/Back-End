import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpRequest, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from App.dto.session_user import SessionUser
from App.models import UserModel
from App.serializers import UserModelSerializer
from App.utils.errors import HttpError, HTTPStatus


# uid의 해당 row값을 리턴
async def get_by_uid(uid) -> UserModel:
    try:
        return UserModel.objects.get(uid=uid)
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)


# email의 해당 row값을 리턴
async def get_by_email(email):
    try:
        row = UserModel.objects.get(email=email)
        return row
    except UserModel.DoesNotExist:
        return None


# 해당 uid의 row값을 삭제
async def delete_by_uid(uid):
    User = await get_by_uid(uid)
    await User.delete()


# UserModel의 전체 필드를 JSON으로 만들어줌
async def serialize():
    query_set = UserModel.objects.all()
    serializer = UserModelSerializer(query_set, many=True)
    json = JSONRenderer.render(serializer.data)
    return json


# UserModel의 필드에서 uid가 일치하는 row값을 JSON으로 리턴해줌
async def serialize_user(req):
    data = JSONParser().parse(req)
    query_set = await get_by_uid(data.get("uid"))
    if query_set.DoesNotExist:
        return JsonResponse("해당 uid가 존재하지 않습니다.", status=404)
    serializer = UserModelSerializer(query_set)
    json = JSONRenderer.render(serializer.data)
    return json


# 회원 가입 시 유저의 정보를 DB에 저장
async def user_register(req):
    data = JSONParser().parse(req)
    uid = uuid.uuid4()
    email = data.get("email")
    pwd = make_password(data.get("pwd"))

    newUserModel = UserModel()
    newUserModel.uid = uid
    newUserModel.email = email
    newUserModel.pwd = pwd

    check_result = UserModel.objects.filter(email=newUserModel.email)

    if check_result.exists():
        raise HttpError(HTTPStatus.CONFLICT, "이미 존재하는 계정입니다.")
    newUserModel.save()


# 회원탈퇴시
async def user_withdraw(session_user: SessionUser, delete_info):
    email = delete_info.get("email")
    pwd = delete_info.get("pwd")
    user = await get_by_email(email)
    if (
        user is None
        or str(user.uid) != session_user.uid
        or not check_password(pwd, user.pwd)
    ):
        raise HttpError(HTTPStatus.UNAUTHORIZED)

    user.delete()


# email과 pwd로 계정 확인
# 2중 데이터베이스 접근 문제가 있어서 확인중
# 현재 쓰고 있지 않음.
# async def check_user(req):
#     data = JSONParser().parse(req)
#     _email = data.get('email')
#     _pwd = data.get('pwd')

#     #_email로 계정을 들고온 후 비밀번호 확인
#     row = await get_by_email(_email)
#     if row==False:
#         return JsonResponse('해당 email이 존재하지 않습니다.',status=404)
#     if not check_password(row.pwd,_pwd):
#         return True
#     else:
#         return False


# req의 session에 user의 uid 값을 저장
def sign_in(req: HttpRequest, user: UserModel, pwd: str) -> SessionUser:
    if not check_password(pwd, user.pwd):
        raise HttpError(HTTPStatus.UNAUTHORIZED, "비밀번호가 일치하지 않습니다.")
    session_user = SessionUser.fromUser(user)
    session_user.save(req.session)
    return session_user


# 해당유저의 req의 session을 빈자리로 만듬.
def sign_out(session):
    SessionUser.clear(session)


# 해당 유저가 현재 로그인이 되어있는지 확인.
def get_signed_user(req: HttpRequest) -> SessionUser | None:
    user = SessionUser.from_session(req.session)
    return user


def check_email(row_email, email):
    if row_email == email:
        return True
    else:
        return False

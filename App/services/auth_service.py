from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from App.models import UserModel
from App.serializers import UserModelSerializer
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus
import uuid
from django.contrib.auth.hashers import make_password, check_password

#uid의 해당 row값을 리턴
async def get_by_uid(uid) -> UserModel:
    try:
        return await UserModel.objects.get(uid = uid)
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)
    
#email의 해당 row값을 리턴
async def get_by_email(email) -> UserModel:
    try:
        return await UserModel.objects.get(email = email)
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)
    

#해당 uid의 row값을 삭제
async def delete_by_uid(uid):
    User = await get_by_uid(uid)
    await User.delete()
    
#UserModel의 전체 필드를 JSON으로 만들어줌
async def serialize():
    query_set = UserModel.objects.all()
    serializer = UserModelSerializer(query_set,many=True)
    json = JSONRenderer.render(serializer.data)
    return json

#UserModel의 필드에서 uid가 일치하는 row값을 JSON으로 리턴해줌
async def serialize_uid(req):
    data = JSONParser().parse(req)
    query_set = await get_by_uid(data.get('uid'))
    if query_set.DoesNotExist:
        return JsonResponse('해당 uid가 존재하지 않습니다.',status=404)
    serializer = UserModelSerializer(query_set)
    json = JSONRenderer.render(serializer.data)
    return json


#회원 가입 시 유저의 정보를 DB에 저장
async def user_register(req):
    data = JSONParser().parse(req)
    uid = uuid.uuid4()
    email = data.get('email')
    pwd = make_password(data.get('pwd'))
    
    newUserModel = UserModel()
    newUserModel.uid = uid
    newUserModel.email = email
    newUserModel.pwd = pwd
    
    newUserModel.save()
    
#회원탈퇴시
async def user_withdraw(req):
    if await check_user(req):
        data = JSONParser().parse(req)
        email = data.get('email')
        row = await get_by_email(email)
        row.delete()
        
        return JsonResponse("회원탈퇴성공",status=201)
    else:
        return HttpResponse(404)

#email과 pwd로 계정 확인
async def check_user(req):
    data = JSONParser().parse(req)
    _email = data.get('email')
    _pwd = data.get('pwd')
    
    #_email로 계정을 들고온 후 비밀번호 확인
    row = await get_by_email(_email)
    if row.DoesNotExist:
        return JsonResponse('해당 email이 존재하지 않습니다.',status=404)
    if not check_password(row.pwd,_pwd):
        return True
    else:
        return False
    
#해당유저를 이메일로 찾고 req의 session에 uid 값을 저장
async def session_save_uid(req:HttpRequest):
    data = JSONParser.parse(req)
    row = UserModel.objects.get(email = data.get('email'))
    req.session['user'] = row.uid
    
    
#해당유저의 req의 session을 빈자리로 만듬.
async def session_delete_uid(req:HttpRequest):
    req.session['user'] = ''
    
    

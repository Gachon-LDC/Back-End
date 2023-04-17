from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from App.models import UserModel
from App.serializers import UserModelSerializer
from django.http import HttpRequest

# Controller
def auth_controller(req):
    if req.method == "GET":
        return get_signed_user(req)
        
    # etc...
    if req.method =="PUT":
        return register(req)
    
    if req.method == "POST":
        return sign_in(req)
    
    if req.method=="DELETE":
        return sign_out(req)

# GET User의 정보를 얻음
def get_signed_user(req:HttpRequest):
    data=JSONParser().parse(req)
    query_set = UserModel.objects.get(email=data.get('email'))
    #쿼리 예외 처리
    if query_set.DoesNotExist:
        return JsonResponse('해당 이메일이 존재 하지 않습니다.',status=201)
    
    serializer = UserModelSerializer(query_set,many=False)
    #serializer 예외 처리
    if serializer.is_valid():
        json=JSONRenderer().render(serializer.data)
        return JsonResponse(json, status=201)
    else:
        return JsonResponse(serializer.errors, status=400)
    

# PUT?? 회원 등록#POST로 수정해서 들고오기
def register(req):
    data=JSONParser().parse(req)
    serializer = UserModelSerializer(data=data)
    if serializer.is_valid():
        json=JSONRenderer().render(serializer.data)
        return JsonResponse(json, status=201)
    else:
        return JsonResponse(serializer.errors, status=401)


# POST 로그인
def sign_in(req):
    data=JSONParser().parse(req)
    check_login=UserModel.objects.get(email=data.get('email'),pwd=data.get('pwd'),salt=data.get('salt'))
    #쿼리 예외 처리
    if check_login.DoesNotExist:
        return JsonResponse('해당 계정이 존재 하지 않습니다.',status=201)


# DELETE 회원 탈퇴//로그 아웃
def sign_out(req):
    data=JSONParser().pares(req)
    query_set = UserModel.objects.filter(email=data.get('email'))
    #쿼리 예외 처리
    if query_set.DoesNotExist:
        return JsonResponse('해당 이메일이 존재 하지 않습니다.',status=201)
    
    serializer = UserModelSerializer(query_set,many=False);
    #시리얼라이저 예외 처리
    if serializer.is_valid():
        query_set.delete()
        json=JSONRenderer().render(serializer.data)
        return JsonResponse(json, status=201)
    else:
        return JsonResponse(serializer.errors,status=401)
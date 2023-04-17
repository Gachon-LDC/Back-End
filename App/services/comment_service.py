from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from App.models import CommentModel
from App.models import UserModel, VideoModel
from App.serializers import UserModelSerializer
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus
import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.core.serializers.json import DjangoJSONEncoder
import json


#email의 해당 row값을 리턴
async def get_by_uid(uid): 
    try:
        row = CommentModel.objects.get(uid = uid)
        return row
    except CommentModel.DoesNotExist:
        return False
    
async def get_by_writerId(writerId):
    try:
        rows = CommentModel.objects.filter(wrtierId=writerId)
        return rows
    except CommentModel.DoesNotExist:
        return False
    
async def get_by_videoId(videoId):
    try:
        rows = CommentModel.objects.filter(videoId = videoId)
        return rows
    except CommentModel.DoesNotExist:
        return False
    
#접근한 사람의 uid와 댓글을 쓴 사람의 uid를 비교해서
#올바르게 접근했다면 해당 rows 를 반환
#아니면 잘못된 접근
async def check_correct_access(req:HttpRequest):
    writerId = req.session.get("user")
    rows = get_by_writerId(writerId)#writerId가 쓴 모든 rows들을 추출
    if rows==False: return False
    writerId_values = rows.values_list('writerId',flat=True)#writerId들만 추출
    writerId_value = writerId_values[0]#한가지 writerId를 추출
    if writerId == writerId_value:#쓴 사람과 접근한 사람이 같다면 rows들을 리턴
        return rows
    else:
        return False

#댓글을 데이터베이스에 저장
async def comment_register(req:HttpRequest):
    data = JSONParser().parse(req)
    uid = uuid.uuid4()
    writerId = req.session.get("user")
    videoId = data.get("videoId")
    content = data.get("content")
    
    if writerId is None or videoId is None or content is None:
        return HttpResponse("Json 양식이 잘못됐습니다.")
    
    writer = UserModel.objects.get(uid = writerId)
    
    #*************************************#
    #테스트 할려고 video모델을 만들어서 넣어줌
    #*************************************#
    print("여기까지 들어왔어요!!2222")
    video_obj = VideoModel(video_id = uuid.uuid4(),title = "asdf")
    video_obj.save()
    
    newCommentModel = CommentModel()
    newCommentModel.uid = uid
    newCommentModel.writerId = writer
    newCommentModel.videoId = video_obj
    newCommentModel.content = content
    
    newCommentModel.save()
    
    print("여기까지 접근했음!!")
    return HttpResponse("댓글 생성 성공", status=201)

#해당 유저가 현재 로그인이 되어있는지 확인.
def check_log_in(req:HttpRequest):
    if req.session['user']!='':
        return True
    else:
        return False
from App.utils.errors import HttpError, HTTPStatus
from App.models import DanceCategoryModel
from App.serializers import DanceCategoryModelSerializer
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
import uuid
from django.http import HttpResponse


async def get_by_id(uid) -> DanceCategoryModel:
    try:
        row = DanceCategoryModel.objects.get(uid=uid)
        return row
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)
        
    
async def get_all(req):
    try:
        rows = DanceCategoryModel.objects.all()
        return rows
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)
    

def check_log_in(req:HttpRequest):
    if req.session['user']!='':
        return True
    else:
        return False
    
async def dance_category_register(req:HttpRequest):
    data = JSONParser().parse(req)
    uid = uuid.uuid4()
    title = data.get("title")
    
    if title is None:
        return HttpResponse("Json 양식이 잘못됐습니다.")
    
    newDanceCategoryModel = DanceCategoryModel()
    newDanceCategoryModel.uid = uid
    newDanceCategoryModel.title = title
    
    newDanceCategoryModel.save()
    
    print("여기까지 접근 성공")
    return HttpResponse("코멘트 생성 성공", status=201)
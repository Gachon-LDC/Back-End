from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from App.models import VideoModel
from App.serializers import UserDanceSerializer, VideoModelSerializer
from django.views.decorators.csrf import csrf_exempt
import base64
from App.apps import SaveFile
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# Create your views here.

image_folder_count = 0

@csrf_exempt
#여기는 원작자가 춤을 등록하는 부분
def register_dance(request):
    if request.method == 'GET':
        query_set = VideoModel.objects.all()
        serializer = VideoModelSerializer(query_set, many = True)
        return JsonResponse(serializer.data, safe=False)
        
        
    if request.method == 'POST': #
        print(request)
        data = JSONParser().parse(request)
        print(data)
        serializer = VideoModelSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            # 여기에 코드 반환을 하면 될듯
            return JsonResponse(serializer.data, status=201)
        
        
        return JsonResponse(serializer.data, status=401)

#춤을 배우길 원하는 플레이어가 원하는 부분이다.
def learn_dance(request):
    global image_folder_count
    
    if request.method =='POST':
        data = JSONParser().parse(request)
        
        #이미지 파일 디코딩한 값
        decode_result = base64.b64decode(data["image"])
        
        #SaveFile.save_file_at_dir('./App/'+data["user_id"]+'/'+str(image_folder_count)+'/', str(data["image_id"])+'_Test.png', decode_result)
        #image_folder_count =image_folder_count
        
        serializer = UserDanceSerializer(data=data)
        
        base64_decoded = base64.b64decode(data["image"])
        image = Image.open(io.BytesIO(base64_decoded))
        image_np = np.array(image)
        plt.imshow(image_np)
        plt.show()
        
        if serializer.is_valid() and serializer.get('end_image') == True:   # serializer가 유효하고, end_image값이 True일대 밑의 문장이 실행됨. 
            #serializer.save()
            return JsonResponse(serializer.validated_data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
        
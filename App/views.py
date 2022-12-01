from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from App.models import VideoModel
from App.serializers import UserDanceSerializer, VideoModelSerializer
from django.views.decorators.csrf import csrf_exempt
import base64
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import cv2
from .compare import compare
# Create your views here.

image_folder_count = 0


@csrf_exempt
# 여기는 원작자가 춤을 등록하는 부분
def register_dance(request):
    if request.method == 'GET':
        query_set = VideoModel.objects.all()
        serializer = VideoModelSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        if serializer.is_valid():
            # 여기에 코드 반환을 하면 될듯
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.data, status=401)

# 춤을 배우길 원하는 플레이어가 원하는 부분이다.


def learn_dance(request):
    global image_folder_count

    data = JSONParser().parse(request)

    if request.method != 'POST' or 'image' not in data:
        return JsonResponse(serializer.errors, status=400)
    else:
        # 이미지 파일 디코딩한 값
        #SaveFile.save_file_at_dir('./App/'+data["user_id"]+'/'+str(image_folder_count)+'/', str(data["image_id"])+'_Test.png', decode_result)
        #image_folder_count =image_folder_count
        serializer = UserDanceSerializer(data=data)
        print(data['image'])
        base64_decoded = base64.b64decode(data["image"])
        image = Image.open(io.BytesIO(base64_decoded))
        image_np = np.array(image)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
        cos = compare(image_np, image_np.copy())
        return JsonResponse({'sim': cos}, status=201)

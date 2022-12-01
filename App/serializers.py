from rest_framework import serializers
from App.models import VideoModel, UserDance
import os


class VideoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields=['__all__']
        
        
        
class UserDanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserDance
        fields=['video_id','user_id','image_id','image','end_image']
        
        
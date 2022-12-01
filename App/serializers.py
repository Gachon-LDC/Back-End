from rest_framework import serializers
from App.models import VideoModel, UserDance, ImageUpload
import os


class VideoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields=['__all__']
        
        
        
class UserDanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserDance
        fields=['video_id','user_id','image_id','image','end_image']
        
    def get(self,content):
        if self.is_valid():
            return self.data[content]
        else:
            return "error: this serializer is not valid"     
        
        
class ImageUploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImageUpload
        fields=['title','text','image']
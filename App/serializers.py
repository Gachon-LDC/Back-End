from rest_framework import serializers
from App.models import VideoModel
from App.models import UserModel

class UserModelSerializer(serializers.ModelSerializer):
    uid=serializers.UUIDField(required=False)
    
    class Meta:
        model=UserModel
        exclude=["pwd"]
        
    
    

class VideoModelSerializer(serializers.ModelSerializer):
    video_id = serializers.UUIDField(required=False)
    uploader_id = serializers.PrimaryKeyRelatedField(read_only=True)
    dance = serializers.PrimaryKeyRelatedField(read_only=True)
    fps = serializers.IntegerField(required=False)

    class Meta:
        model = VideoModel
        fields = ["__all__"]
        exclude = ["embeds"]

    pass

from rest_framework import serializers
from App.models import VideoModel
from App.models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False)

    class Meta:
        model = UserModel
        fields = ["__all__"]
        exclude = ["pwd", "salt"]


class VideoModelSerializer(serializers.ModelSerializer):
    video_id = serializers.UUIDField(required=False)
    uploader_id = serializers.UUIDField(read_only=True, required=False)
    dance = serializers.UUIDField(read_only=True, required=False)
    file = serializers.FileField(required=False)

    class Meta:
        model = VideoModel
        fields = "__all__"

    pass

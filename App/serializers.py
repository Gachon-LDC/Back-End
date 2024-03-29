from rest_framework import serializers
from App.models import VideoModel
from App.models import UserModel
from App.models import CommentModel
from App.models import DanceCategoryModel


class UserModelSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False)

    class Meta:
        model = UserModel
        exclude = ["pwd"]


class CommentModelSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False)
    videoId = serializers.UUIDField(required=False)
    writerId = serializers.UUIDField(required=False)
    content = serializers.CharField(required=True)

    class Meta:
        model = CommentModel
        fields = ("uid", "videoId", "writerId", "content")


class DanceCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanceCategoryModel
        fields = ("uid", "title")


class VideoModelSerializer(serializers.ModelSerializer):
    video_id = serializers.UUIDField(required=False)
    uploader_id = serializers.UUIDField(read_only=True, required=False)
    dance = serializers.UUIDField(read_only=True, required=False)
    file = serializers.FileField(required=False)

    class Meta:
        model = VideoModel
        fields = "__all__"

    pass

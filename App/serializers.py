from rest_framework import serializers
from App.models import VideoModel
import os


class VideoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = ["__all__"]

    pass

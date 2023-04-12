from django.db.models import (
    Model,
    UUIDField,
    TextField,
    IntegerField,
    ForeignKey,
)
from django.db import models


class UserModel(Model):
    uid = UUIDField(primary_key=True)
    email = TextField()
    pwd = TextField()
    salt = TextField()


class DanceCategoryModel(Model):
    uid = UUIDField(primary_key=True)
    title = TextField()


# Create your models here.
class VideoModel(Model):
    """file path : static/video/UID"""

    video_id = UUIDField(primary_key=True)
    uploader_id = UUIDField()  # many to one @ User.uid,
    title = TextField()

    dance = UUIDField()
    fps = IntegerField()
    content = TextField(default="")


class VideoAngleModel(Model):
    angle_id = UUIDField(primary_key=True)
    embeds = TextField()
    video_id = UUIDField()


class CommentModel(Model):
    uid = UUIDField(primary_key=True)
    videoId = ForeignKey(VideoModel, on_delete=models.CASCADE)
    writerId = ForeignKey(UserModel, on_delete=models.CASCADE)
    content = TextField()

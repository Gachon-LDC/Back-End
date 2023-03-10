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
    salt = TextField


class DanceCategoryModel(Model):
    uid = UUIDField(primary_key=True)
    title = TextField()


# Create your models here.
class VideoModel(Model):
    video_id = UUIDField(primary_key=True)
    uploader_id = ForeignKey(
        UserModel, on_delete=models.SET_NULL, null=True
    )  # many to one @ User.uid,
    file_path = TextField()  # file Path
    embeds = TextField()
    dance = ForeignKey(DanceCategoryModel, on_delete=models.PROTECT)
    fps = IntegerField()


class CommentModel(Model):
    uid = UUIDField(primary_key=True)
    videoId = ForeignKey(VideoModel, on_delete=models.CASCADE)
    writerId = ForeignKey(UserModel, on_delete=models.CASCADE)
    content = TextField()

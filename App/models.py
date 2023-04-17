from django.db.models import (
    Model,
    UUIDField,
    TextField,
    IntegerField,
    ForeignKey,
)
from django.db import models
import uuid


class UserModel(Model):
    uid = UUIDField(primary_key=True,default = uuid.uuid4)
    email = TextField()
    pwd = TextField()


class DanceCategoryModel(Model):
    uid = UUIDField(primary_key=True,default = uuid.uuid4)
    title = TextField()


# Create your models here.
class VideoModel(Model):
    """file path : static/video/UID"""

    video_id = UUIDField(primary_key=True,default = uuid.uuid4)
    
    uploader_id = ForeignKey(
        UserModel, on_delete=models.SET_NULL, null=True
    )  # many to one @ User.uid,
    
    title = TextField()
    embeds = TextField()
    dance = ForeignKey(DanceCategoryModel, on_delete=models.PROTECT)
    fps = IntegerField()
    content = TextField()


class CommentModel(Model):
    uid = UUIDField(primary_key=True,default = uuid.uuid4)
    videoId = UUIDField(default = uuid.uuid4)
    writerId = UUIDField(default = uuid.uuid4)
    content = TextField()

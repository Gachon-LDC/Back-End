from django.db.models import (
    Model,
    UUIDField,
    TextField,
    IntegerField,
)
import uuid


class UserModel(Model):
    uid = UUIDField(primary_key=True, default=uuid.uuid4)
    email = TextField()
    pwd = TextField()


class DanceCategoryModel(Model):
    uid = UUIDField(primary_key=True, default=uuid.uuid4)
    title = TextField()


# Create your models here.
class VideoModel(Model):
    """file path : static/video/UID"""

    video_id = UUIDField(primary_key=True)
    uploader_id = UUIDField()  # many to one @ User.uid,
    title = TextField()
    dance = UUIDField(null=True)  # many to one @ Category.uid,
    content = TextField(default="")


class VideoAngleModel(Model):
    embeds = TextField()
    video_id = UUIDField(primary_key=True)
    fps = IntegerField()


class CommentModel(Model):
    uid = UUIDField(primary_key=True, default=uuid.uuid4)
    videoId = UUIDField(default=uuid.uuid4)
    writerId = UUIDField(default=uuid.uuid4)
    content = TextField()

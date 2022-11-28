from django.db.models import (
    Model,
    UUIDField,
    TextField,
    JSONField,
    IntegerField,
    FileField,
)

# Create your models here.
class VideoModel(Model):
    id = UUIDField()
    uploader_id = TextField()
    post_id = TextField()
    angles = JSONField()
    # meta data
    path = FileField()
    video_lenghth = IntegerField()
    fps = IntegerField()

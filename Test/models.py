from django.db import models

# Create your models here.

class Test(models.Model):
    Video_id = models.UUIDField(primary_key=True)
    uploader_id = models.TextField()
    post_id = models.TextField()
    angles = models.JSONField()
    # meta data
    path = models.FileField()
    video_lenghth = models.IntegerField()
    fps = models.IntegerField()
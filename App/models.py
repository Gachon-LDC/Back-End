from django.db.models import (
    Model,
    UUIDField,
    TextField,
    JSONField,
    IntegerField,
    FileField,
    BooleanField,
)

# Create your models here.
class VideoModel(Model):
    video_id = UUIDField(primary_key=True) 
    uploader_id = TextField()  
    post_id = TextField()       
    angles = JSONField()    
    # meta data
    path = FileField()    
    video_lenghth = IntegerField()
    fps = IntegerField()           


class UserDance(Model):
    video_id = UUIDField(primary_key=True)
    user_id = UUIDField()
    image_id = IntegerField()
    image = TextField()
    end_image = BooleanField(default=False)
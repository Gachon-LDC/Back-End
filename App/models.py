from django.db.models import (
    Model,
    UUIDField,
    TextField,
    JSONField,
    IntegerField,
    FileField,
    BooleanField,
    CharField,
    ImageField
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
    video_id = UUIDField()
    user_id = UUIDField()
    image_id = IntegerField(primary_key=True)
    image = TextField()
    end_image = BooleanField(default=False)
    
    
class ImageUpload(Model):
    title = CharField(max_length=200)
    text = TextField()
    image = ImageField(upload_to="%Y/%m/%d")
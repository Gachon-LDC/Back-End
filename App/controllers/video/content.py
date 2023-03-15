# /video/[video id]
from django.http import HttpResponse


def content_controller(req, video_id):
    return HttpResponse(f"content controller id : {video_id}")


# GET(id) /video/[video id]
def video_info(req, id):
    pass


# DELETE(id)
def delete_video(req, id):
    pass


# PUT(id)
def update_video_info(req, id):
    pass

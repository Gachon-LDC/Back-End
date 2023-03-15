from django.http import HttpResponse


# /video/[video id]/learn
def learn_controller(req, video_id):
    return HttpResponse(f"learn controller id : {video_id}")


# POST(id) /video/[video id]/learn
def compare_frame(req, id):
    pass

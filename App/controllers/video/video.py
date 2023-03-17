from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework import status
from App.models import VideoModel
from App.serializers import VideoModelSerializer
from App.utils.utils import int_or_0
from App.utils.errors import HttpError, HTTPStatus, HttpErrorHandling


@HttpErrorHandling
def video_controller(req: HttpRequest):
    """video Controller
    url : /video
    """
    match (req.method):
        case "GET":
            return video_list(req)
        case "POST":
            return upload_video(req)
        case _:
            raise HttpError(HTTPStatus.NOT_FOUND)


async def video_list(req: HttpRequest):
    """_summary_ get VideoList
    ### Params
    offset : Optional[int]
    limit : Optional[int]
    """
    offset = int_or_0(req.GET.get("offset"))
    limit = int_or_0(req.GET.get("limit", 10))

    videos = await VideoModel.objects.all()[offset : offset + limit]
    serailized = VideoModelSerializer(videos, many=True)
    return JsonResponse(serailized, ensure_ascii=True)


# POST
async def upload_video(req: HttpRequest):
    """
    _summary_ Update Video Info
    Method: POST
    """
    del req.body["video_id"]
    video = VideoModelSerializer(data=req.body)
    if not video.is_valid():
        return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    saved = await upload_video(video)

    return JsonResponse(saved, ensure_ascii=True)

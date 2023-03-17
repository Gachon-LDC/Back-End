from django.http import HttpRequest, JsonResponse, HttpResponse
from App.serializers import VideoModelSerializer

from App.services import video_service
from App.utils.errors import HttpErrorHandling, HttpError, HTTPStatus


@HttpErrorHandling
async def content_controller(req: HttpRequest, video_id: str):
    """_summary_ video_item_controller
    url : /video/[video_id]
    """
    match req.method:
        case "GET":
            return await video_info(req, video_id)
        case "DELETE":
            return delete_video(req, video_id)
        case "PUT":
            return update_video_info(req, video_id)
        case "_":
            raise HttpError(HTTPStatus.NOT_FOUND)


async def video_info(_: HttpRequest, video_id: str):
    """_summary_ GET controller
    return : video information of video id
    """
    ret = await video_service.get_by_id(video_id)
    serialized = VideoModelSerializer(ret)
    serialized.is_valid()
    return JsonResponse(serialized.validated_data, ensure_ascii=True)


async def delete_video(req: HttpRequest, video_id: str):
    """_summary_ DELETE video"""
    user_id = "#TODO: get signed User Info from auth service"
    await video_service.delete_by_id(video_id, user_id)
    return HttpResponse("success")


async def update_video_info(req: HttpRequest, video_id: str):
    """_summary_ PUT update video"""
    serializer = VideoModelSerializer(req.body)
    serializer.is_valid()
    user_id = "#TODO: get signed User Info from auth service"
    await video_service.update_video(video_id, user_id, serializer.validated_data)
    return HttpResponse("success")

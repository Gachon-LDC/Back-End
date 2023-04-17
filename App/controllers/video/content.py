from django.http import HttpRequest, JsonResponse, HttpResponse
from App.serializers import VideoModelSerializer

from App.services import video_service
from App.utils.IController import IController


class ContentController(IController):
    """_summary_ video_item_controller
    url : /video/[video_id]
    """

    http_method_names = ["get", "post", "delete", "put", "patch"]

    async def get(self, _: HttpRequest, video_id: str):
        """_summary_ GET controller
        return : video information of video id
        """
        ret = await video_service.get_by_id(video_id)
        serialized = VideoModelSerializer(ret)
        return JsonResponse(serialized.data)

    async def put(self, req: HttpRequest, video_id: str):
        """_summary_ PUT update video"""
        serializer = VideoModelSerializer(req.body)
        serializer.is_valid()
        user_id = "#TODO: get signed User Info from auth service"
        await video_service.update_video(video_id, user_id, serializer.validated_data)
        return HttpResponse("success")

    async def delete(self, _: HttpRequest, video_id: str):
        """_summary_ DELETE video"""
        user_id = "#TODO: get signed User Info from auth service"
        await video_service.delete_by_id(video_id, user_id)
        return HttpResponse("success")

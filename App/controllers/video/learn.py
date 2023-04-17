from django.http import HttpRequest, JsonResponse
from App.utils.errors import HttpError, HTTPStatus
from App.services import angle_service, learn_service
from App.utils.IController import IController


class LearnController(IController):
    """_summary_ learn dance movement Controler
    url : /video/[video_id]/learn
    """

    async def get(req: HttpRequest, video_id: str):
        """_summary_ POST compare frame\n
        check current frame's simirarity

        if not signed : throw unauthorized error
        """
        image = req.POST.get("image")

        # TODO: check request user is signed

        if "image" == None:
            raise HttpError(HTTPStatus.UNPROCESSABLE_ENTITY)

        video = await angle_service.get_by_id(video_id)
        np_image = learn_service.cvt_base64_2_np(image)

        simirarity = learn_service.compare_from_frame(np_image, video, 0)
        return JsonResponse({"simirarity": simirarity})

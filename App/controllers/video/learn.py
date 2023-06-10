from django.http import HttpRequest, JsonResponse
from App.services import angle_service, learn_service
from App.utils.errors import HttpError, HTTPStatus
from App.utils.IController import IController
from App.dto.session_user import SessionUser


class LearnController(IController):
    """_summary_ learn dance movement Controler
    url : /video/[video_id]/learn
    """

    async def post(self, req: HttpRequest, video_id: str):
        """_summary_ POST compare frame\n
        check current frame's simirarity

        if not signed : throw unauthorized error
        """
        if SessionUser.from_session(req.session) is None:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "로그인이 필요합니다.")
        image = req.FILES.get("image")
        nframe = req.POST.get("nframe")
        if (
            nframe is None
            or image is None
            or image.content_type not in ["image/jpeg", "image/png"]
        ):
            raise HttpError(HTTPStatus.UNPROCESSABLE_ENTITY)

        video = await angle_service.get_by_id(video_id)
        np_image = learn_service.image2np(image)

        simirarity = learn_service.compare_from_frame(np_image, video, int(nframe))
        return JsonResponse({"simirarity": simirarity, "fps": video.fps})

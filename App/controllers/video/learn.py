from django.http import HttpRequest, JsonResponse
from App.utils.errors import HttpErrorHandling, HttpError, HTTPStatus
from App.services import video_service, learn_service


@HttpErrorHandling
async def learn_controller(req: HttpRequest, video_id: str):
    """_summary_ learn dance movement Controler
    url : /video/[video_id]/learn
    """
    match req.method:
        case "POST":
            return await compare_frame(req, video_id)
        case "_":
            raise HttpError(HTTPStatus.NOT_FOUND)


async def compare_frame(req: HttpRequest, video_id: str):
    """_summary_ POST compare frame\n
    check current frame's simirarity

    if not signed : throw unauthorized error
    """
    image = req.POST.get("image")

    # TODO: check request user is signed

    if "image" == None:
        raise HttpError(HTTPStatus.UNPROCESSABLE_ENTITY)

    video = await video_service.get_by_id(video_id)
    np_image = learn_service.cvt_base64_2_np(image)

    simirarity = learn_service.compare_from_frame(np_image, video, 0)
    return JsonResponse({"simirarity": simirarity})

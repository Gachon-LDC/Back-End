from django.http import HttpRequest
from App.utils.errors import HttpErrorHandling, HttpError, HTTPStatus
from App.services import video_service, learn_service


@HttpErrorHandling
def learn_controller(req: HttpRequest, video_id: str):
    """_summary_ learn dance movement Controler
    url : /video/[video_id]/learn
    """
    match req.method:
        case "POST":
            return compare_frame(req, video_id)
        case "_":
            raise HttpError(HTTPStatus.NOT_FOUND)


def compare_frame(req: HttpRequest, video_id: str):
    """_summary_ POST compare frame\n
    check current frame's simirarity

    if not signed : throw unauthorized error
    """
    user_id = "#TODO: get signed User Info from auth service"
    # video = video_service.get_by_id(video_id)
    image = req.POST.get("image")
    np_image = learn_service.cvt2np_image(image)
    cos = learn_service.compare(np_image, np_image.copy())
    pass

from django.http import HttpRequest
from App.utils.errors import HttpErrorHandling, HttpError, HTTPStatus


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
    pass

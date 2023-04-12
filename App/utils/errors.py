from http import HTTPStatus
from django.http import HttpResponse


class HttpError(Exception):
    """_summary_ Error Point for HTTP Error management

    Args:
        http_status (HTTPStatus): http Status
        msg (Optional[str]) : message for http error
    """

    def __init__(self, http_status: HTTPStatus | int, msg: str = "") -> None:
        self.msg = msg
        if isinstance(http_status, HTTPStatus):
            self.status = http_status.value
            if self.msg == "":
                self.msg = http_status.phrase
        else:
            self.status = http_status

    def response(self):
        return HttpResponse(self.msg, status=self.status)


def HttpErrorHandling(func):
    """decorator for handling HttpProccessing Error on endpoint"""

    async def Inner_Function(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HttpError as e:
            return e.response()

    return Inner_Function

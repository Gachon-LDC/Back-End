from django.http import HttpRequest, HttpResponse
from django.views import View
from .errors import HttpError


class IController(View):
    async def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            return await super().dispatch(request, *args, **kwargs)
        except HttpError as e:
            return e.response

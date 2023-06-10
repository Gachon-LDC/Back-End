from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .errors import HttpError


class IController(View):
    async def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            return await super().dispatch(request, *args, **kwargs)
        except HttpError as e:
            return e.response()
        except ObjectDoesNotExist as e:
            return HttpResponse(status=404)
        except ValidationError as e:
            if "UUID" in e.__str__():
                return HttpResponse(status=404)
            return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(status=500)

from django.http import HttpResponse, Http404

# Create your views here.

image_folder_count = 0


def index(req):
    if req.method == "GET":
        return HttpResponse("LDC backeand api")
    else:
        raise Http404()

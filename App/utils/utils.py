import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def int_or_0(s: str | None | int):
    if s is None:
        return 0
    try:
        return int(s)
    finally:
        return 0


def save_files(path, uuid, extension, file):
    """
    Args:
        path (_type_): file path name
        uuid (_type_): file uuid
        extension (_type_): file extension
        file (_type_): file object
    Returns:
        str: file path
    """
    dir = os.path.join(settings.MEDIA_ROOT, path)
    save_path = os.path.join(dir, f"{uuid}.{extension}")
    storage = FileSystemStorage()
    storage.save(save_path, file)
    return save_path

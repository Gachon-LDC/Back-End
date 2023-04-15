import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from threading import Thread


def int_or_0(s: str | None | int):
    if s is None:
        return 0
    try:
        return int(s)
    finally:
        return 0


class FilePath:
    def __init__(self, type, uuid, extension) -> None:
        """
        path (_type_): file path name
        uuid (_type_): file uuid
        extension (_type_): file extension
        """
        dir = os.path.join(settings.MEDIA_ROOT, type)
        self.name = os.path.join(dir, f"{uuid}.{extension}")

    def save(self, file):
        """save file on f/s"""
        storage = FileSystemStorage()
        storage.save(self.name, file)

    def save_thread(self, file) -> Thread:
        """save file on f/s with thread"""
        thread = Thread(target=self.save, args=(file))
        thread.start()
        return thread

    def delete(self):
        """delete file from f/s"""
        storage = FileSystemStorage()
        storage.delete(self.name)

    def delete_thread(self) -> Thread:
        """delete file from f/s with thread"""
        thread = Thread(target=self.delete)
        thread.start()
        return thread

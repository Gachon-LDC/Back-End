from uuid import UUID, uuid4

from django.db import IntegrityError

from App.models import VideoModel
from App.serializers import VideoModelSerializer
from App.utils import FilePath
from App.utils.errors import HttpError, HTTPStatus

from . import angle_service


async def get_by_id(pk) -> VideoModel:
    """(async) get video by id"""
    try:
        return await VideoModel.objects.aget(pk=pk)
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)


async def get_by_category(category_id) -> VideoModel:
    """(async) get video by category"""
    return VideoModel.objects.filter(dance=category_id)


def is_writer_or_403(user_id, video: VideoModel):
    if str(video.uploader_id) != str(user_id):
        raise HttpError(HTTPStatus.UNAUTHORIZED)


async def delete_by_id(pk, user_id: str):
    """(async) delete video by id"""
    video = await get_by_id(pk)
    is_writer_or_403(user_id, video)
    angle_del = angle_service.delete_angle(pk)
    VideoModel.delete(video)
    file = FilePath("video", pk, "mp4")
    file.delete_thread()
    await angle_del


async def update_video(
    pk, user_id: str, update_info: VideoModel | VideoModelSerializer
):
    """(async) update video infomation"""
    video = await get_by_id(pk)
    is_writer_or_403(user_id, video)
    if update_info.content is not None:
        video.content = update_info.content
    if update_info.title is not None:
        video.title = update_info.title
    video.save()


async def save_video(
    uploader_id: UUID | str, new_video: VideoModel | VideoModelSerializer, file
):
    if isinstance(new_video, VideoModelSerializer):
        new_video = VideoModel(**new_video.data)
    new_video.video_id = uuid4()
    new_video.uploader_id = uploader_id
    new_video.dance = uuid4()
    try:
        angle_service.save_predicted_video(new_video, file)
        await new_video.asave()
        deseralizer = VideoModelSerializer(new_video)
        return deseralizer.data
    except IntegrityError:
        raise HttpError(
            HTTPStatus.INTERNAL_SERVER_ERROR, "Retry Required (uuid conflict)"
        )

from App.utils.errors import HttpError, HTTPStatus
from App.models import VideoModel
from App.serializers import VideoModelSerializer


async def get_by_id(pk) -> VideoModel:
    """(async) get video by id"""
    try:
        return await VideoModel.objects.aget(pk=pk)
    except:
        raise HttpError(HTTPStatus.NOT_FOUND)


def is_writer_or_403(user_id, video: VideoModel):
    if video.uploader_id.pk != user_id:
        raise HttpError(HTTPStatus.UNAUTHORIZED)


async def delete_by_id(pk, user_id: str):
    """(async) delete video by id"""
    video = await get_by_id(pk)
    is_writer_or_403(user_id, video)
    video.delete()
    # TODO: delete from F/S


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


def save_video(new_video: VideoModel | VideoModelSerializer):
    # TODO: check UUID is automatically generated?
    new_video.save()
    # TODO : save video file
    # save file

    # return video full information

    seralizer = VideoModelSerializer(new_video)
    seralizer.is_valid()

    return seralizer.validated_data

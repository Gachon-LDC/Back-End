from django.db import IntegrityError
from App.services.model_predict import predict_pose, VideoReader
from App.utils.errors import HttpError, HTTPStatus
from App.utils.utils import FilePath
from App.models import VideoModel, VideoAngleModel
from App.serializers import VideoModelSerializer
from uuid import uuid4, UUID
from threading import Thread
import cv2


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
    video_del = video.adelete()
    angle = await VideoAngleModel.objects.aget(pk=pk)
    angle_del = angle.adelete()
    file = FilePath("video", pk, "mp4")
    file.delete_thread()
    await video_del
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


def save_predicted_video(video: VideoModel, file):
    file_path = FilePath("video", video.video_id, "mp4")
    file_path.save(file)
    video_reader = VideoReader(file_path.name)
    result = predict_pose(video_reader)

    cap = cv2.VideoCapture(file_path.name)
    fps = cap.get(cv2.CAP_PROP_FPS)

    angle_model = VideoAngleModel()
    angle_model.video_id = video.video_id
    angle_model.embeds = result.angles
    angle_model.fps = fps
    angle_model.save()
    pass


async def save_video(
    uploader_id: UUID, new_video: VideoModel | VideoModelSerializer, file
):
    if isinstance(new_video, VideoModelSerializer):
        new_video = VideoModel(**new_video.data)
    new_video.video_id = uuid4()
    new_video.uploader_id = uploader_id
    new_video.dance = uuid4()
    try:
        await new_video.asave()
        thread = Thread(target=save_predicted_video, args=(new_video, file))
        thread.start()
        deseralizer = VideoModelSerializer(new_video)
        return deseralizer.data
    except IntegrityError:
        raise HttpError(
            HTTPStatus.INTERNAL_SERVER_ERROR, "Retry Required (uuid conflict)"
        )

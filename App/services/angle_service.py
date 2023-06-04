from threading import Thread

import cv2

from App.models import VideoAngleModel, VideoModel
from App.utils import FilePath

from .model_predict import VideoReader, predict_pose


def __save_predict_video(video, file):
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


def save_predicted_video(video: VideoModel, file) -> Thread:
    thread = Thread(target=__save_predict_video, args=(video, file))
    thread.start()
    return thread


async def delete_angle(id):
    angle = await VideoAngleModel.objects.aget(pk=id)
    await angle.adelete()


async def get_by_id(id):
    angle = await VideoAngleModel.objects.aget(pk=id)
    return angle

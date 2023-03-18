import base64
import io

import cv2
import numpy as np
from PIL import Image

from App.models import VideoModel
from App.services.model_compare import get_angle, cos_sim
import json

def cvt_base64_2_np(image: str):
    """convert base64 image to PIL.Image"""
    base64_decoded = base64.b64decode(image)
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
    return image_np


def compare_from_frame(
    img: np.ndarray, video: VideoModel, frame_num: int
) -> float:
    embeds = json.loads(video.embeds)
    angle1 = embeds[frame_num]
    angle2 = get_angle(img)
    
    return cos_sim(angle1, angle2)

import base64
import io

import cv2
import numpy as np
from PIL import Image

from App.models import VideoAngleModel
from App.services.model_compare import get_angle, cos_sim
import json

EMBED_CHECK_SIZE = 1


def cvt_base64_2_np(image: str):
    """convert base64 image to PIL.Image"""
    base64_decoded = base64.b64decode(image)
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
    return image_np


def compare_from_frame(
    img: np.ndarray, angle: VideoAngleModel, frame_num: int
) -> float:
    embeds = json.loads(angle.embeds)

    check_offset = max([0, frame_num - EMBED_CHECK_SIZE])
    check_last = max([frame_num + EMBED_CHECK_SIZE, len(embeds)])
    angle = get_angle(img)
    sim = float("-inf")
    for embed in embeds[check_offset:check_last]:
        cur = cos_sim(angle, embed)
        if sim < cur:
            sim = cur

    return sim

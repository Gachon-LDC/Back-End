import base64
import io

import cv2
import numpy as np
from PIL import Image


from .compare import compare
__all__ = ["cvt_base64_2_np", "compare"]



def cvt_base64_2_np(image):
    """convert base64 image to PIL.Image"""
    base64_decoded = base64.b64decode(image)
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
    return image_np


if __name__ == "__main__":
    impath = cv2.imread("./move1.jpeg")
    impath2 = cv2.imread("./move1_compare1.jpeg")
    cos = compare(impath, impath2, isfile=True)
    print(cos)

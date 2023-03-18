import numpy as np

from .predict import POST_NET, ImageReader, predict_pose


def map_norm_item(item_list):
    ret = []
    for item in item_list:
        ret.append({"value": item, "norm": np.linalg.norm(item)})
    return ret


def cos_sim(a, b):
    a_nalue_norm = map_norm_item(a)
    b_nalue_norm = map_norm_item(b)
    max_sim = 0

    for a in a_nalue_norm:
        for b in b_nalue_norm:
            sim = np.divide(
                np.dot(a["value"], b["value"]), np.multiply(a["norm"], b["norm"])
            )
            if sim > max_sim:
                max_sim = sim
    return max_sim


def compare(image1: np.ndarray, image2: np.ndarray, isfile=False):
    """calc simirarity from 2 np images"""
    frame_provider = ImageReader([image1], isfile=isfile)
    angle0 = predict_pose(POST_NET, frame_provider, cpu=True).angles[0]
    frame_provider2 = ImageReader([image2], isfile=isfile)
    angle1 = predict_pose(POST_NET, frame_provider2, cpu=True).angles[0]
    cos = cos_sim(angle0, angle1)
    return cos


if __name__ == "__main__":
    impath = "./move1.jpeg"
    impath2 = "./move1_compare1.jpeg"
    cos = compare(impath, impath2, isfile=True)
    print(cos)

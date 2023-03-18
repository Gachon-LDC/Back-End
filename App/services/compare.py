import numpy as np
from numpy import dot
from numpy.linalg import norm

from .predict import POST_NET, ImageReader, predict_ret_pose_frame




def map_norm_item(item_list):
    ret = []
    for item in item_list:
        ret.append({"value": item, "norm": norm(item)})
    return ret


def cos_sim(a, b):
    a_nalue_norm = map_norm_item(a)
    b_nalue_norm = map_norm_item(b)
    max_sim = 0

    for a in a_nalue_norm:
        for b in b_nalue_norm:
            sim = np.divide(
                dot(a["value"], b["value"]), np.multiply(a["norm"], b["norm"])
            )
            if sim > max_sim:
                max_sim = sim
    return max_sim


def compare(image1, image2, isfile=False):
    frame_provider = ImageReader([image1], isfile=isfile)
    _, angles, _ = predict_ret_pose_frame(POST_NET, frame_provider, cpu=True)
    frame_provider2 = ImageReader([image2], isfile=isfile)
    _, angles_2, _ = predict_ret_pose_frame(POST_NET, frame_provider2, cpu=True)
    cos = cos_sim(angles[0], angles_2[0])
    return cos


if __name__ == "__main__":
    impath = "./move1.jpeg"
    impath2 = "./move1_compare1.jpeg"
    cos = compare(impath, impath2, isfile=True)
    print(cos)

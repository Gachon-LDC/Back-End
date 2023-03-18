import numpy as np

from .model_predict import POST_NET, ImageReader, predict_pose


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


def get_angle(image: np.ndarray, angle_idx=0, isfile=False):
    frame_provider = ImageReader([image], isfile=isfile)
    angle = predict_pose(POST_NET, frame_provider).angles[angle_idx]
    return angle


if __name__ == "__main__":
    impath = "./move1.jpeg"
    impath2 = "./move1_compare1.jpeg"
    angle1 = get_angle(impath, isfile=True)
    angle2 = get_angle(impath, isfile=True)
    cos = cos_sim(angle1, angle2)
    print(cos)

import sys
from os import path
from numpy import dot
from numpy.linalg import norm
import torch


sys.path.append(path.abspath("./pose_net"))
from pose.models.with_mobilenet import PoseEstimationWithMobileNet
from pose.modules.load_state import load_state
from predict import CHECKPOINT, ImageReader, predict_ret_pose_frame


impath = "./move1.jpeg"
impath2 = "./move1_compare1.jpeg"


def cos_sim(a, b):

    b_norms = [norm(b_item) for b_item in b]
    max_sim = 0

    for a_item in a:
        a_norm = norm(a)
        for i, b_norm in enumerate(b_norms):
            sim = dot(a_item, b[i]) / (a_norm * b_norm)
            if sim > max_sim:
                max_sim = sim
    return max_sim


def main():
    net = PoseEstimationWithMobileNet()
    checkpoint = torch.load(CHECKPOINT, map_location="cpu")
    load_state(net, checkpoint)
    frame_provider = ImageReader([impath])
    _, angles, _ = predict_ret_pose_frame(net, frame_provider)
    frame_provider2 = ImageReader([impath2])
    _, angles_2, _ = predict_ret_pose_frame(net, frame_provider2)
    cos = cos_sim(angles[0], angles_2[0])
    print(cos)


# main()

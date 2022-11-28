import sys
from os import path
import argparse
from typing import Any
import json
import cv2
import numpy as np
import torch

import pandas as pd
from matplotlib import pyplot


sys.path.append(path.abspath("./pose_net"))
from pose.models.with_mobilenet import PoseEstimationWithMobileNet
from pose.modules.keypoints import extract_keypoints, group_keypoints
from pose.modules.load_state import load_state
from pose.modules.pose import Pose, track_poses
from pose.val import normalize, pad_width


CHECKPOINT = "./model_weight.pth"


class ImageReader(object):
    def __init__(self, file_names):
        self.file_names = file_names
        self.max_idx = len(file_names)

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx == self.max_idx:
            raise StopIteration
        img = cv2.imread(self.file_names[self.idx], cv2.IMREAD_COLOR)
        if img.size == 0:
            raise IOError("Image {} cannot be read".format(self.file_names[self.idx]))
        self.idx = self.idx + 1
        return img


class VideoReader(object):
    def __init__(self, file_name):
        self.file_name = file_name
        try:  # OpenCV needs int to read from webcam
            self.file_name = int(file_name)
        except ValueError:
            pass

    def __iter__(self):
        self.cap = cv2.VideoCapture(self.file_name)
        if not self.cap.isOpened():
            raise IOError("Video {} cannot be opened".format(self.file_name))
        return self

    def __next__(self):
        was_read, img = self.cap.read()
        if not was_read:
            raise StopIteration
        return img


def infer_fast(
    net,
    img,
    net_input_height_size,
    stride,
    upsample_ratio,
    cpu,
    pad_value=(0, 0, 0),
    img_mean=np.array([128, 128, 128], np.float32),
    img_scale=np.float32(1 / 256),
):
    height, width, _ = img.shape
    scale = net_input_height_size / height

    scaled_img = cv2.resize(
        img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR
    )
    scaled_img = normalize(scaled_img, img_mean, img_scale)
    min_dims = [net_input_height_size, max(scaled_img.shape[1], net_input_height_size)]
    padded_img, pad = pad_width(scaled_img, stride, pad_value, min_dims)

    tensor_img = torch.from_numpy(padded_img).permute(2, 0, 1).unsqueeze(0).float()
    if not cpu:
        tensor_img = tensor_img.cuda()

    stages_output = net(tensor_img)

    stage2_heatmaps = stages_output[-2]
    heatmaps = np.transpose(stage2_heatmaps.squeeze().cpu().data.numpy(), (1, 2, 0))
    heatmaps = cv2.resize(
        heatmaps,
        (0, 0),
        fx=upsample_ratio,
        fy=upsample_ratio,
        interpolation=cv2.INTER_CUBIC,
    )

    stage2_pafs = stages_output[-1]
    pafs = np.transpose(stage2_pafs.squeeze().cpu().data.numpy(), (1, 2, 0))
    pafs = cv2.resize(
        pafs,
        (0, 0),
        fx=upsample_ratio,
        fy=upsample_ratio,
        interpolation=cv2.INTER_CUBIC,
    )

    return heatmaps, pafs, scale, pad


def calc_angle(p1, p2, p3):
    pt1 = p1 - p2
    pt2 = p3 - p2
    ang1 = np.arctan2(pt1[1], pt1[0])
    ang2 = np.arctan2(pt2[1], pt2[0])
    ang = np.rad2deg((ang2 - ang1))
    ang = np.abs(ang)
    # if ang > 360:
    #     ang = 360 - ang
    return ang


def get_angles(key_points):
    r_sho = calc_angle(key_points[1], key_points[2], key_points[3])
    l_sho = calc_angle(key_points[1], key_points[5], key_points[6])
    r_neck_up = calc_angle(key_points[0], key_points[1], key_points[2])
    l_neck_up = calc_angle(key_points[0], key_points[1], key_points[5])
    r_nect_down = calc_angle(key_points[2], key_points[1], key_points[8])
    l_nect_down = calc_angle(key_points[5], key_points[1], key_points[11])
    r_elbo = calc_angle(key_points[2], key_points[3], key_points[4])
    l_elbo = calc_angle(key_points[5], key_points[6], key_points[7])
    l_hip = calc_angle(key_points[1], key_points[11], key_points[12])
    r_hip = calc_angle(key_points[1], key_points[8], key_points[9])
    l_knee = calc_angle(key_points[11], key_points[12], key_points[13])
    r_knee = calc_angle(key_points[8], key_points[9], key_points[10])
    return [
        r_sho,
        l_sho,
        r_neck_up,
        l_neck_up,
        r_nect_down,
        l_nect_down,
        r_elbo,
        l_elbo,
        l_hip,
        r_hip,
        l_knee,
        r_knee,
    ]


def draw_angles(img, pose, angles):
    (
        r_sho,
        l_sho,
        r_neck_up,
        l_neck_up,
        r_nect_down,
        l_nect_down,
        r_elbo,
        l_elbo,
        l_hip,
        r_hip,
        l_knee,
        r_knee,
    ) = angles
    cv2.rectangle(
        img,
        (pose.bbox[0], pose.bbox[1]),
        (pose.bbox[0] + pose.bbox[2], pose.bbox[1] + pose.bbox[3]),
        (0, 255, 0),
    )
    cv2.putText(
        img,
        str(int(r_sho)),
        pose.keypoints[2],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )

    cv2.putText(
        img,
        str(int(l_sho)),
        pose.keypoints[5],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )

    cv2.putText(
        img,
        f"{int(r_neck_up)}  {int(l_neck_up)}",
        pose.keypoints[1] + [-25, 0],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )

    cv2.putText(
        img,
        f"{int(r_nect_down)}  {int(l_nect_down)}  ",
        pose.keypoints[1] + [-25, 20],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )

    cv2.putText(
        img,
        f"{int(r_elbo)}",
        pose.keypoints[3],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )
    cv2.putText(
        img,
        f"{int(l_elbo)}",
        pose.keypoints[6],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )
    cv2.putText(
        img,
        f"{int(l_hip)}",
        pose.keypoints[11],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )
    cv2.putText(
        img,
        f"{int(r_hip)}",
        pose.keypoints[8],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )
    cv2.putText(
        img,
        f"{int(l_knee)}",
        pose.keypoints[12],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )

    cv2.putText(
        img,
        f"{int(r_knee)}",
        pose.keypoints[9],
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )


def predict_ret_pose_frame(
    net, image_provider, cpu=False, track=False, smooth=False, display=False, save=False
):
    net = net.eval()
    if not cpu:
        net = net.cuda()
    # height_size = 256
    height_size = 128
    stride = 8
    upsample_ratio = 4
    num_keypoints = Pose.num_kpts
    previous_poses = []
    predicted_frames = []
    predicted_poses = []
    predicted_angles = []
    for img in image_provider:
        orig_img = img.copy()
        heatmaps, pafs, scale, pad = infer_fast(
            net, img, height_size, stride, upsample_ratio, cpu
        )

        total_keypoints_num = 0
        all_keypoints_by_type = []
        for kpt_idx in range(num_keypoints):  # 19th for bg
            total_keypoints_num += extract_keypoints(
                heatmaps[:, :, kpt_idx], all_keypoints_by_type, total_keypoints_num
            )

        pose_entries, all_keypoints = group_keypoints(all_keypoints_by_type, pafs)
        for kpt_id in range(all_keypoints.shape[0]):
            all_keypoints[kpt_id, 0] = (
                all_keypoints[kpt_id, 0] * stride / upsample_ratio - pad[1]
            ) / scale
            all_keypoints[kpt_id, 1] = (
                all_keypoints[kpt_id, 1] * stride / upsample_ratio - pad[0]
            ) / scale
        current_poses = []
        for n in range(len(pose_entries)):
            if len(pose_entries[n]) == 0:
                continue
            pose_keypoints = np.ones((num_keypoints, 2), dtype=np.int32) * -1
            for kpt_id in range(num_keypoints):
                if pose_entries[n][kpt_id] != -1.0:  # keypoint was found
                    pose_keypoints[kpt_id, 0] = int(
                        all_keypoints[int(pose_entries[n][kpt_id]), 0]
                    )
                    pose_keypoints[kpt_id, 1] = int(
                        all_keypoints[int(pose_entries[n][kpt_id]), 1]
                    )
            pose = Pose(pose_keypoints, pose_entries[n][18])
            current_poses.append(pose)

        poses = []
        angles = []
        for pose in current_poses:
            cur_angles = get_angles(pose.keypoints)
            angles.append(cur_angles)

            if display or save:
                draw_angles(img, pose, cur_angles)
            if save:
                poses.append(pose.keypoints.tolist())

            pp = pd.DataFrame(pose.keypoints, columns=["x", "y"])
            pp["name"] = pose.kpt_names

        if display or save:
            if track:
                track_poses(previous_poses, current_poses, smooth=smooth)
                previous_poses = current_poses
            for pose in current_poses:
                pose.draw(img)
            img = cv2.addWeighted(orig_img, 0.6, img, 0.4, 0)

        predicted_frames.append(img)
        predicted_poses.append(poses)
        predicted_angles.append(angles)
        if display:
            cur = img.copy()
            cv2.cvtColor(cur, cv2.COLOR_BGR2RGB, cur)
            pyplot.imshow(cur)
            pyplot.show(block=False)
            pyplot.pause(0.00001)
            pyplot.clf()
    return predicted_poses, predicted_angles, predicted_frames


def save_result(args, video_mode, poses, angles, frames):
    outPath = "./out"
    if not video_mode:
        name = args.images[0].split("/")[-1]
        name = ".".join(name.split(".")[:-1])
        out_file_name = "out_" + name[-1]
        cv2.imwrite(path.join(outPath + out_file_name + ".jpg"), frames[0])
        with open(out_file_name + ".json", "w") as f:
            json.dump(poses, f)
        with open(out_file_name + ".json", "w") as f:
            json.dump(angles, f)
        return
    file_name = args.video
    try:
        file_name = int(file_name)
    except:
        name = file_name.split("/")[-1]
        name = ".".join(name.split(".")[:-1])
        out_file_name = "out" + name

    finally:
        cap = cv2.VideoCapture(file_name)
        out = cv2.VideoWriter(
            out_file_name + ".mp4",
            fourcc=cv2.VideoWriter_fourcc(*"mp4v"),
            fps=cap.get(cv2.CAP_PROP_FPS),
            frameSize=(
                int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            ),
        )
        for frame in frames:
            out.write(frame)
        out.release()
        with open(out_file_name + ".json", "w") as f:
            json.dump(poses, f)
        with open(out_file_name + ".json", "w") as f:
            json.dump(angles, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Lightweight human pose estimation python demo.
                       This is just for quick results preview.
                       Please, consider c++ demo for the best performance."""
    )
    parser.add_argument(
        "--images", nargs="+", default="", help="path to input image(s)"
    )
    parser.add_argument(
        "--video", type=str, default="", help="path to video file or camera id"
    )
    parser.add_argument(
        "--cpu", action="store_true", help="run network inference on cpu"
    )
    parser.add_argument("--save", action="store_true", help="save predicted result")
    parser.add_argument(
        "--display", action="store_true", help="display predicted result"
    )
    parser.add_argument("--track", type=int, default=1, help="track pose id in video")
    parser.add_argument("--smooth", type=int, default=1, help="smooth pose keypoints")
    args = parser.parse_args()

    if args.video == "" and args.images == "":
        raise ValueError("Either --video or --image has to be provided")

    net = PoseEstimationWithMobileNet()
    checkpoint = torch.load(CHECKPOINT, map_location="cpu")
    load_state(net, checkpoint)
    video_mode = False
    if args.images != "":
        frame_provider: Any = ImageReader(args.images)
    else:
        video_mode = True
        frame_provider = VideoReader(args.video)

    poses, angles, frames = predict_ret_pose_frame(
        net, frame_provider, args.cpu, args.track, args.smooth, args.display, args.save
    )
    if args.save:
        save_result(args, video_mode, poses, angles, frames)

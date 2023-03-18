import sys
from os import path
from typing import Any

import cv2
import numpy as np
import pandas as pd
import torch

sys.path.append(path.abspath("App/pose_net"))
from ..pose_net.models.with_mobilenet import PoseEstimationWithMobileNet
from ..pose_net.modules.keypoints import extract_keypoints, group_keypoints
from ..pose_net.modules.load_state import load_state
from ..pose_net.modules.pose import Pose, track_poses
from ..pose_net.val import normalize, pad_width

# region load Model
__CHECKPOINT = "./model/weight.pth"
POST_NET = PoseEstimationWithMobileNet()
POST_NET = POST_NET.eval()
load_state(POST_NET, torch.load(__CHECKPOINT, map_location="cpu"))
# endregion


class ImageReader(object):
    def __init__(self, images, isfile=True):
        self.images = images
        self.max_idx = len(images)
        self.isfile = isfile

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx == self.max_idx:
            raise StopIteration
        img = (
            cv2.imread(self.images[self.idx], cv2.IMREAD_COLOR)
            if self.isfile
            else self.images[self.idx]
        )
        if img.size == 0:
            raise IOError("Image {} cannot be read".format(self.images[self.idx]))
        self.idx = self.idx + 1
        return img


class VideoReader(object):
    def __init__(self, file_name):
        try:  # OpenCV needs int to read from webcam
            self.file_name = int(file_name)
        except ValueError:
            self.file_name = file_name

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


class Angle:
    def __init__(self, key_points) -> None:
        self.r_sho = self.calc_angle(key_points[1], key_points[2], key_points[3])
        self.l_sho = self.calc_angle(key_points[1], key_points[5], key_points[6])
        self.r_neck_up = self.calc_angle(key_points[0], key_points[1], key_points[2])
        self.l_neck_up = self.calc_angle(key_points[0], key_points[1], key_points[5])
        self.r_nect_down = self.calc_angle(key_points[2], key_points[1], key_points[8])
        self.l_nect_down = self.calc_angle(key_points[5], key_points[1], key_points[11])
        self.r_elbo = self.calc_angle(key_points[2], key_points[3], key_points[4])
        self.l_elbo = self.calc_angle(key_points[5], key_points[6], key_points[7])
        self.l_hip = self.calc_angle(key_points[1], key_points[11], key_points[12])
        self.r_hip = self.calc_angle(key_points[1], key_points[8], key_points[9])
        self.l_knee = self.calc_angle(key_points[11], key_points[12], key_points[13])
        self.r_knee = self.calc_angle(key_points[8], key_points[9], key_points[10])

    def list(self):
        return [
            self.r_sho,
            self.l_sho,
            self.r_neck_up,
            self.l_neck_up,
            self.r_nect_down,
            self.l_nect_down,
            self.r_elbo,
            self.l_elbo,
            self.l_hip,
            self.r_hip,
            self.l_knee,
            self.r_knee,
        ]

    def calc_angle(self, p1, p2, p3):
        pt1 = p1 - p2
        pt2 = p3 - p2
        ang1 = np.arctan2(pt1[1], pt1[0])
        ang2 = np.arctan2(pt2[1], pt2[0])
        ang = np.rad2deg((ang2 - ang1))
        ang = np.abs(ang)
        return ang


class PredictResult:
    def __init__(self, save=False) -> None:
        self.poses: list[Any] = []
        self.angles: list[Any] = []
        if save:
            self.frames: list[Any] = []
        self.save = save

    def append(self, poses, angles, img: np.ndarray):
        if self.save:
            self.frames.append(img)
        self.poses.append(poses)
        self.angles.append(angles)


def infer_fast(
    net,
    img,
    net_input_height_size,
    stride,
    upsample_ratio=4,
    pad_value=(0, 0, 0),
    img_mean=np.array([128, 128, 128], np.float32),
    img_scale=np.float32(1 / 256),
    cpu=True,
):
    height, _, _ = img.shape
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


def put_text(image, text, position):
    cv2.putText(
        image,
        text,
        position,
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (0, 0, 255),
    )


def draw_frame(img, pose, angle: Angle):
    cv2.rectangle(
        img,
        (pose.bbox[0], pose.bbox[1]),
        (pose.bbox[0] + pose.bbox[2], pose.bbox[1] + pose.bbox[3]),
        (0, 255, 0),
    )
    put_text(
        img,
        f"{int(angle.r_neck_up)}  {int(angle.l_neck_up)}",
        pose.keypoints[1] + [-25, 0],
    )
    put_text(
        img,
        f"{int(angle.r_nect_down)}  {int(angle.l_nect_down)}  ",
        pose.keypoints[1] + [-25, 20],
    )
    put_text(img, str(int(angle.r_sho)), pose.keypoints[2])
    put_text(img, f"{int(angle.r_elbo)}", pose.keypoints[3])
    put_text(img, str(int(angle.l_sho)), pose.keypoints[5])
    put_text(img, f"{int(angle.l_elbo)}", pose.keypoints[6])
    put_text(img, f"{int(angle.r_hip)}", pose.keypoints[8])
    put_text(img, f"{int(angle.r_knee)}", pose.keypoints[9])
    put_text(img, f"{int(angle.l_hip)}", pose.keypoints[11])
    put_text(img, f"{int(angle.l_knee)}", pose.keypoints[12])


def display_frame(img: np.ndarray):
    pyplot.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    pyplot.show(block=False)
    pyplot.pause(0.00001)
    pyplot.clf()


def predict_pose(
    image_provider, track=False, smooth=False, display=False, save=False
) -> PredictResult:
    """_summary_ predict post shape

    Returns:
        list[np.ndarray] : listof keyPoints
        list[flaot] : listof angles
        list[np.ndarray] : listof frame that angle annotated
    """
    height_size = 128
    stride = 8
    upsample_ratio = 4
    num_keypoints = Pose.num_kpts
    previous_poses: list[Any] = []
    result = PredictResult(save)
    for img in image_provider:
        orig_img = img.copy()
        heatmaps, pafs, scale, pad = infer_fast(POST_NET, img, height_size, stride)

        total_keypoints_num = 0
        all_keypoints_by_type: list[Any] = []
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
            current_poses.append(Pose(pose_keypoints, pose_entries[n][18]))

        poses, angles = [], []
        for pose in current_poses:
            cur_angles = Angle(pose.keypoints)
            angles.append(cur_angles.list())

            if display or save:
                draw_frame(img, pose, cur_angles)
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
            if display:
                display_frame(img)
        result.append(poses, angles, img)
    return result


def save_result(args, video_mode, result: PredictResult):
    if not video_mode:
        name = args.images[0].split("/")[-1]
        name = ".".join(name.split(".")[:-1])
        out_file_name = "./out_" + name[-1]
        cv2.imwrite(path.join(out_file_name + ".jpg"), result.frames[0])
        with open(out_file_name + ".json", "w") as f:
            json.dump(result.poses, f)
        with open(out_file_name + ".json", "w") as f:
            json.dump(result.angles, f)
        return
    file_name = args.video
    try:
        name = file_name
        file_name = int(file_name)
    except:
        name = file_name.split("/")[-1]
        name = ".".join(name.split(".")[:-1])

    finally:
        out_file_name = "./out" + name
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
        for frame in result.frames:
            out.write(frame)
        out.release()
        with open(out_file_name + ".json", "w") as f:
            json.dump(result.poses, f)
        with open(out_file_name + ".json", "w") as f:
            json.dump(result.angles, f)


if __name__ == "__main__":
    import argparse
    import json

    from matplotlib import pyplot

    # region parse cli arg
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
    parser.add_argument("--save", action="store_true", help="save predicted result")
    parser.add_argument(
        "--display", action="store_true", help="display predicted result"
    )
    parser.add_argument("--track", type=int, default=1, help="track pose id in video")
    parser.add_argument("--smooth", type=int, default=1, help="smooth pose keypoints")
    # endregion
    if (args := parser.parse_args()).video == "" and args.images == "":
        raise ValueError("Either --video or --image has to be provided")

    video_mode = False
    if args.images != "":
        frame_provider: Any = ImageReader(args.images)
    else:
        video_mode = True
        frame_provider = VideoReader(args.video)

    result = predict_pose(
        frame_provider,
        args.track,
        args.smooth,
        args.display,
        args.save,
    )
    if args.save:
        save_result(args, video_mode, result)

import os
from typing import List
import cv2


class FrameData:
    def __init__(self, frame_name: str, coordinates: tuple, time_process: float):
        self.frame_name = frame_name
        self.coordinates = coordinates
        self.time_process = time_process


class SceneData:
    def __init__(self, scene_name: str):
        self.scene_name = scene_name
        self.frames: List[FrameData] = []

    def add_frame_data(self, frame_data: FrameData):
        self.frames.append(frame_data)

    def add_frames_data(self, frames_data: List[FrameData]):
        self.frames.extend(frames_data)

    def gen_scene_path(self, base_path: str) -> str:
        scene_path = os.path.join(base_path, self.scene_name)
        if not os.path.exists(scene_path):
            os.makedirs(os.path.abspath(scene_path))
        return scene_path


class CamData:
    def __init__(self, cam_name: str, cam_src: str, cam_cap: cv2.VideoCapture):
        self.cam_name = cam_name
        self.cam_src = cam_src
        self.cam_cap = cam_cap
        self.scenes: List[SceneData] = []

    def add_scene_data(self, scene_data: SceneData):
        self.scenes.append(scene_data)

    def gen_cam_by_scene_path(self, base_path: str, scene_data: SceneData) -> str:
        scene_path = scene_data.gen_scene_path(base_path)
        cam_path = os.path.join(scene_path, self.cam_name + ".txt")
        if not os.path.exists(cam_path):
            with open(cam_path, 'w'):
                pass
        return cam_path

    def construct_cam_data_by_scene(self, scene_data: SceneData) -> str:
        result = ""
        for frame in scene_data.frames:
            result += f"{frame.frame_name}, {frame.coordinates}, {frame.time_process}"

            # add new line
            result += "\n"
        return result

    def export_cam_data(self, base_path: str):
        for scene in self.scenes:
            cam_w_scene_path = self.gen_cam_by_scene_path(base_path, scene)
            with open(cam_w_scene_path, 'w') as file:
                cam_data = self.construct_cam_data_by_scene(scene)
                file.write(cam_data)

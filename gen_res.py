import os
from typing import List

RESULT_ROOT_PATH = "results/PRIVATE_TEST"
RESULT_ROOT_PATH_TEST = "results/test_export"

is_test = True
if is_test:
    RESULT_ROOT_PATH = RESULT_ROOT_PATH_TEST


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

    def gen_scene_path(self) -> str:
        scene_path = os.path.join(RESULT_ROOT_PATH, self.scene_name)
        if not os.path.exists(scene_path):
            os.makedirs(os.path.abspath(scene_path))
        return scene_path


class CamData:
    def __init__(self, cam_name: str):
        self.cam_name = cam_name
        self.scenes: List[SceneData] = []

    def add_scene_data(self, scene_data: SceneData):
        self.scenes.append(scene_data)

    def gen_cam_by_scene_path(self, scene_data: SceneData) -> str:
        scene_path = scene_data.gen_scene_path()
        cam_path = os.path.join(scene_path, self.cam_name + ".txt")
        if not os.path.exists(cam_path):
            with open(cam_path, 'w') as file:
                pass
        return cam_path

    def construct_cam_data_by_scene(self, scene_data: SceneData) -> str:
        result = ""
        for frame in scene_data.frames:
            result += f"{frame.frame_name}, {frame.coordinates}, {frame.time_process}"

            # add new line
            result += "\n"
        return result

    def export_cam_data(self):
        for scene in self.scenes:
            cam_w_scene_path = self.gen_cam_by_scene_path(scene)
            with open(cam_w_scene_path, 'w') as file:
                cam_data = self.construct_cam_data_by_scene(scene)
                file.write(cam_data)


# used for testing
if __name__ == '__main__':
    cam1 = CamData("CAM_1")
    scene1_cam1 = SceneData("SCENE_1")

    cam1.add_scene_data(scene1_cam1)
    scene1_cam1.add_frames_data([
        FrameData(
            "frame_1.jpg",
            (0,0,1,2),
            0.3
        ),
        FrameData(
            "frame_2.jpg",
            (0, 0, 1, 3),
            1
        )
    ])
    cam1.export_cam_data()

    cam2 = CamData("CAM_2")
    scene1_cam2 = SceneData("SCENE_1")

    cam2.add_scene_data(scene1_cam2)
    scene1_cam2.add_frames_data([
        FrameData(
            "frame_1.jpg",
            (0, 0, 1, 2),
            6
        ),
        FrameData(
            "frame_2.jpg",
            (0, 0, 1, 3),
            5
        )
    ])
    scene2_cam2 = SceneData("SCENE_2")

    cam2.add_scene_data(scene2_cam2)
    scene2_cam2.add_frames_data([
        FrameData(
            "frame_1.jpg",
            (0, 0, 1, 2),
            100
        ),
        FrameData(
            "frame_2.jpg",
            (0, 0, 1, 3),
            5
        )
    ])
    cam2.export_cam_data()

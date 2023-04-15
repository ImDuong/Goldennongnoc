import os
from typing import List
from models.media import CamData, SceneData, FrameData

# used for testing
if __name__ == '__main__':
    # set test path
    RESULT_ROOT_PATH = "results/test_export"

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
    cam1.export_cam_data(RESULT_ROOT_PATH)

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
    cam2.export_cam_data(RESULT_ROOT_PATH)

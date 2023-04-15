import os.path

from lib.utils import vertices_detector
from models.media import CamData, SceneData, FrameData
import matplotlib.pyplot as plt
import itertools

RESULT_ROOT_PATH = "../results/test_greyscale_overlapping_area"
AREA1_IMG_PATH = "../assets/sample_greyscale_overlapping_area/area1.png"
AREA2_IMG_PATH = "../assets/sample_greyscale_overlapping_area/area2.png"

if __name__ == '__main__':
    img1 = plt.imread(AREA1_IMG_PATH)[:, :, 0]

    vertices = vertices_detector(img1)

    cam1 = CamData("CAM_1")
    scene1_cam1 = SceneData("SCENE_1")

    cam1.add_scene_data(scene1_cam1)
    scene1_cam1.add_frames_data([
        FrameData(
            os.path.basename(AREA1_IMG_PATH),
            tuple(itertools.chain(*vertices)),
            0.3
        ),
    ])
    cam1.export_cam_data(RESULT_ROOT_PATH)

    img2 = plt.imread(AREA2_IMG_PATH)[:, :, 0]

    vertices = vertices_detector(img2)

    cam2 = CamData("CAM_2")
    scene1_cam2 = SceneData("SCENE_1")

    cam2.add_scene_data(scene1_cam2)
    scene1_cam2.add_frames_data([
        FrameData(
            os.path.basename(AREA2_IMG_PATH),
            tuple(itertools.chain(*vertices)),
            0.3
        ),
    ])
    cam2.export_cam_data(RESULT_ROOT_PATH)

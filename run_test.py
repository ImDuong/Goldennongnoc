import os

from lib.iou import calculate_IOU_btw_files
from models.media import CamData, SceneData, FrameData

CAMERA_TEST_ID = {}
CAMERA_GROUND_TRUTH_ID = {}
SCENE_GROUND_TRUTH_ID = {}

CAMERA_SAMPLE_STATISTICS = {
    2: {
        "nb_scenes": 0,
        "ious": [],
    },
    3: {
        "nb_scenes": 0,
        "ious": [],
    },
    4: {
        "nb_scenes": 0,
        "ious": [],
    },
}


def load_test_data(camera_name: str, scene_name: str):
    if CAMERA_TEST_ID.get(camera_name) is not None:
        pass
    else:
        CAMERA_TEST_ID[camera_name] = CamData(camera_name)
    scene_inst = SceneData(scene_name)
    CAMERA_TEST_ID[camera_name].add_scene_data(scene_inst)


def load_ground_truth_data(camera_name: str, scene_name: str):
    if CAMERA_GROUND_TRUTH_ID.get(camera_name) is not None:
        pass
    else:
        CAMERA_GROUND_TRUTH_ID[camera_name] = CamData(camera_name)
    scene_inst = SceneData(scene_name)
    CAMERA_GROUND_TRUTH_ID[camera_name].add_scene_data(scene_inst)


def iterate_data(data_path: str, load_func):
    root_list = os.listdir(data_path)
    for scene_name in root_list:
        scene_path = os.path.join(data_path, scene_name)
        if os.path.isdir(scene_path):
            SCENE_GROUND_TRUTH_ID[scene_name] = True

            camera_list = os.listdir(scene_path)
            for camera in camera_list:
                camera_path = os.path.join(scene_path, camera)
                if os.path.isfile(camera_path):
                    camera_name = os.path.splitext(camera)[0]
                    load_func(camera_name, scene_name)


DATASET_PATH = "./assets/Public_Test/videos/"
GROUND_TRUTH_DATASET_PATH = "./assets/Public_Test/groundtruth"
RESULT_PATH = "./results/Public_Test"

if __name__ == '__main__':
    # load data
    iterate_data(DATASET_PATH, load_test_data)
    iterate_data(GROUND_TRUTH_DATASET_PATH, load_ground_truth_data)

    # predict

    # export results
    for cam in CAMERA_TEST_ID:
        cam.export_cam_data(RESULT_PATH)

    # compare prediction from exported results with ground truth
    print(">>> IOU for each scene")
    for scene_name in SCENE_GROUND_TRUTH_ID:
        scene_path = os.path.join(GROUND_TRUTH_DATASET_PATH, scene_name)
        camera_list = os.listdir(scene_path)

        # scene IOU is the average IOU of all cameras' IOU
        scene_IOU = 0
        for camera in camera_list:
            camera_path = os.path.join(scene_path, scene_name)
            if os.path.isfile(camera_path):
                # camera IOU is the average IOU of all frames in that camera's video
                camera_IOU = 0
                camera_name = os.path.splitext(camera)[0]

                test_camera_result_path = os.path.join(RESULT_PATH, scene_name, camera_name + ".txt")
                ground_truth_camera_result_path = camera_path

                if not os.path.exists(test_camera_result_path):
                    print("camera result is missing", test_camera_result_path)
                    camera_IOU = 0
                else:
                    camera_IOU = calculate_IOU_btw_files(ground_truth_camera_result_path, test_camera_result_path)
                scene_IOU += camera_IOU
        scene_IOU /= len(camera_list)

        CAMERA_SAMPLE_STATISTICS[len(camera_list)]["nb_scenes"] += 1
        CAMERA_SAMPLE_STATISTICS[len(camera_list)]["ious"].append(scene_IOU)

        print(f"{scene_name}: {scene_IOU}")

    avg_IOU = 0.25 * sum(CAMERA_SAMPLE_STATISTICS[2]["ious"]) / CAMERA_SAMPLE_STATISTICS[2]["nb_scenes"] \
        + 0.3 * sum(CAMERA_SAMPLE_STATISTICS[3]["ious"]) / CAMERA_SAMPLE_STATISTICS[3]["nb_scenes"] \
        + 0.45 * sum(CAMERA_SAMPLE_STATISTICS[4]["ious"]) / CAMERA_SAMPLE_STATISTICS[4]["nb_scenes"]
    print(f">>> Average IOU: {avg_IOU}")

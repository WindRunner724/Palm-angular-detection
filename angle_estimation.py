import cv2 as cv
import numpy as np
import option_parser
import sys
import time
from examination import *
import vis
import mediapipe as mp
from palm_image import PalmImg
from tqdm import tqdm

es_failed_cnt = 0
args = option_parser.get_parser().parse_args()
# args.input_images_path = "../dataset/Save_Data/scenario/test/"
# args.output_images_path = "../dataset/Save_Data/scenario/test/rtl/"
args.input_images_path = "../dataset/plain_angular_test/1/plain/near/"
args.output_images_path = "../dataset/plain_angular_test/1/plain/near/rtl/"
args.kpt_list_path = "../dataset/plain_angular_test/1/plain/near/test_kpt.npy"
args.type = "kpt-to-ir"
args.sample_radius = 5
args.tri_kpt_idx = [0, 9, 13]
args.all_kpt_idx = [0, 1, 2, 5, 9, 13, 17]


# Calculate normal vector angle of intersection
def compute_normal_vec(palm_pair):
    # a, b, c = args.tri_kpt_idx
    coff = 1.0
    pos_2d = palm_pair.kpt_pos_3
    pix_val = palm_pair.kpt_pix_3

    pit_a = np.array([pos_2d[0][0], pos_2d[0][1], coff * pix_val[0]])
    pit_b = np.array([pos_2d[1][0], pos_2d[1][1], coff * pix_val[1]])
    pit_c = np.array([pos_2d[2][0], pos_2d[2][1], coff * pix_val[2]])

    vec_a = pit_b - pit_a
    vec_b = pit_c - pit_a

    norm = np.cross(vec_b, vec_a)
    angle_x = np.arctan(norm[0] / np.sqrt((norm[1] ** 2 + norm[2] ** 2) / 2))
    angle_y = np.arctan(norm[1] / np.sqrt((norm[0] ** 2 + norm[2] ** 2) / 2))
    return [np.degrees(angle_x), np.degrees(angle_y)]


def save_rtl(img, index):
    path_str = args.output_images_path.split("/")
    rtl_img_name = f"rtl_{path_str[2]}_{path_str[3]}_{path_str[4]}_{str(index)}_com.jpg"
    cv.imwrite(os.path.join(args.output_images_path, rtl_img_name), img)


def kpt_estimate(rgb_files):
    global es_failed_cnt
    hands = mp.solutions.hands.Hands(static_image_mode=args.static_image_mode,
                                     max_num_hands=args.max_num_hands,
                                     min_detection_confidence=args.min_detection_confidence,
                                     min_tracking_confidence=args.min_tracking_confidence)
    kpt_list = np.zeros((len(rgb_files), 21, 2))
    for idx, file in enumerate(rgb_files):
        detected_img = cv.imread(os.path.join(args.input_images_path, f"Rgb/{file}"))
        detected_img = cv.cvtColor(detected_img, cv.COLOR_BGR2RGB)
        rtl = hands.process(detected_img).multi_hand_landmarks
        if rtl:
            pos_3d = np.array([[rtl[0].landmark[i].x, rtl[0].landmark[i].y, rtl[0].landmark[i].z]
                               for i in range(len(rtl[0].landmark))])
            # mask = (pos_3d[:, 0] >= 0) & (pos_3d[:, 0] <= 1) & (pos_3d[:, 1] >= 0) & (pos_3d[:, 1] <= 1)
            # pos_3d[~mask] = None
            kpt_list[idx] = pos_3d[:, 0:2]
        else:
            es_failed_cnt += 1
    np.save(os.path.join(args.input_images_path, f"test_kpt.npy"), kpt_list)
    return kpt_list


def process(idx, palm_file, kpt_list):
    # Mediapipe estimation
    palm_img = PalmImg(args=args, palm_path=palm_file, index=idx, sample_radius=args.sample_radius)
    palm_img.set_kpt_21_pos(kpt_list)
    # Sample three points in palm
    palm_img.sample_v1()
    palm_img.set_kpt_21_pix()
    palm_img.set_kpt_3_pix()
    angular = compute_normal_vec(palm_img)
    # Visualize
    rtl_img = palm_img.palm_img.copy()
    vis.vis(img=rtl_img, palm_img=palm_img, angular=angular)
    rtl_img = vis.merge(palm_img, rtl_img)
    save_rtl(img=rtl_img, index=palm_img.index)
    return


def main():
    start_t = time.time()

    # Extract ir palm images list
    palm_files = sorted(os.listdir(args.input_images_path + "Ir"))
    rtl_path = args.output_images_path
    # Ensure output path
    if not os.path.exists(rtl_path):
        os.makedirs(rtl_path)

    if args.type == "rgb-to-ir":
        rgb_files = sorted(os.listdir(args.input_images_path + "Rgb"))
        kpt_list = kpt_estimate(rgb_files)
    elif args.type == "kpt-to-ir":
        kpt_list = np.load(args.kpt_list_path)
        if kpt_list.shape != (len(palm_files), 21, 2):
            raise ValueError("Wrong keypoints npy format")
    else:
        raise ValueError("Wrong input type!")

    # Examine rgb and ir's corresponding
    qualified_num = len(palm_files)
    # try:
    #     qualified_num = exam_id_corr(rgb_list=rgb_files, ir_list=ir_files)
    #     if not qualified_num:
    #         raise ValueError("No corresponding images found!")
    # except ValueError as e:
    #     print(f"Caught an exception: {str(e)}\nPlease check images naming\n")

    # Process
    for i in tqdm(range(len(palm_files))):
        process(idx=i, palm_file=palm_files[i], kpt_list=kpt_list[i])

    end_t = time.time()
    print(f"{qualified_num} total files processed\n"
          f"{es_failed_cnt} estimation failed\n"
          f"{end_t - start_t}s cost")


if __name__ == "__main__":
    main()

import cv2 as cv
import numpy as np
import option_parser
import sys
import time
from examination import *
from multiprocessing import Pool, Value, Lock
import vis
import mediapipe as mp
from paired_image import PairedImg

es_failed_cnt = Value('i', 0)
lock = Lock()
args = option_parser.get_parser().parse_args()
# args.input_images_path = "dataset/Save_Data/scenario/test/"
# args.output_images_path = "dataset/Save_Data/scenario/test/rtl/"
args.input_images_path = "dataset/plain_angular_test/1/bottom/45_near/"
args.output_images_path = "dataset/plain_angular_test/1/bottom/45_near/rtl/"
args.sample_radius = 5
args.tri_kpt_idx = [0, 9, 13]
args.all_kpt_idx = [0, 1, 2, 5, 9, 13, 17]
# Instantiation Hand object of mediapipe
hands = mp.solutions.hands.Hands(static_image_mode=args.static_image_mode,
                                 max_num_hands=args.max_num_hands,
                                 min_detection_confidence=args.min_detection_confidence,
                                 min_tracking_confidence=args.min_tracking_confidence)


# Calculate normal vector angle of intersection
def compute_normal_vec(img_pair):
    # a, b, c = args.tri_kpt_idx
    coff = 1.0
    pos_2d = img_pair.kpt_pos_3
    pix_val = img_pair.kpt_pix_3

    pit_a = np.array([pos_2d[0][0], pos_2d[0][1], coff*pix_val[0]])
    pit_b = np.array([pos_2d[1][0], pos_2d[1][1], coff*pix_val[1]])
    pit_c = np.array([pos_2d[2][0], pos_2d[2][1], coff*pix_val[2]])

    vec_a = pit_b - pit_a
    vec_b = pit_c - pit_a

    norm = np.cross(vec_b, vec_a)
    angle_x = np.arctan(norm[0] / np.sqrt((norm[1]**2 + norm[2]**2)/2))
    angle_y = np.arctan(norm[1] / np.sqrt((norm[0]**2 + norm[2]**2)/2))
    return [np.degrees(angle_x), np.degrees(angle_y)]


def save_rtl(img, index):
    path_str = args.output_images_path.split("/")
    rtl_img_name = f"rtl_{path_str[2]}_{path_str[3]}_{path_str[4]}_{str(index)}_com.jpg"
    cv.imwrite(os.path.join(args.output_images_path, rtl_img_name), img)


def process(files):
    # Mediapipe estimation
    img_pair = PairedImg(args=args, rgb_path=files[0], ir_path=files[1], index=files[2], hands=hands,
                         sample_radius=args.sample_radius)
    if not img_pair.kpt_estimation("RGB"):
        with lock:
            es_failed_cnt.value += 1
        return
    # Sample three points in palm
    img_pair.sample_v1()
    img_pair.set_kpt_21()
    img_pair.set_kpt_3()
    angular = compute_normal_vec(img_pair)
    # Visualize
    rtl_img = img_pair.ir_img.copy()
    vis.vis(img=rtl_img, img_pair=img_pair, angular=angular)
    rtl_img = vis.merge(img_pair, rtl_img)
    save_rtl(img=rtl_img, index=img_pair.index)
    return


def main():
    start_t = time.time()
    # Extract rgb and ir images list
    rgb_files = sorted(os.listdir(args.input_images_path + "Rgb"))
    ir_files  = sorted(os.listdir(args.input_images_path + "Ir"))
    rtl_path  = args.output_images_path
    # Ensure output path
    if not os.path.exists(rtl_path):
        os.makedirs(rtl_path)
    # Examine rgb and ir's corresponding
    qualified_num = 0
    try:
        qualified_num = exam_id_corr(rgb_list=rgb_files, ir_list=ir_files)
        if not qualified_num:
            raise ValueError("No corresponding images found!")
    except ValueError as e:
        print(f"Caught an exception: {str(e)}\nPlease check images naming\n")

    # Test
    # test = [rgb_files[0], ir_files[0], 0]
    # process(test)
    # Process
    img_files = list(zip(rgb_files, ir_files, list(range(len(rgb_files)))))
    with Pool() as p:
        p.map(process, img_files)

    end_t = time.time()
    print(f"{qualified_num} total files processed\n"
          f"{es_failed_cnt.value} estimation failed\n"
          f"{end_t-start_t}s cost")


if __name__ == "__main__":
    main()

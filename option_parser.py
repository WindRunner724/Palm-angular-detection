import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--static_image_mode", type=bool, default=True, help="Whether to treat the input images as a "
                                                                             "batch of static and possibly unrelated "
                                                                             "images, or a video stream")
    parser.add_argument("--min_detection_confidence", type=float, default=0.35, help="Minimum confidence value ([0.0, "
                                                                                     "1.0]) for hand detection to be "
                                                                                     "considered successful")
    parser.add_argument("--min_tracking_confidence", type=float, default=0.35, help="Minimum confidence value ([0.0, "
                                                                                    "1.0]) for the hand landmarks to be"
                                                                                    " considered tracked successfully")
    parser.add_argument("--max_num_hands", type=int, default=1, help="Maximum number of hands to detect")
    parser.add_argument("--input_images_path", type=str, default="../dataset/ir/1", help="The path to images need "
                                                                                         "proceed")
    parser.add_argument("--output_images_path", type=str, default="../dataset/ir/1_rtl", help="The path to save output")
    parser.add_argument("--kpt_list_path", type=str, default="../dataset", help="The path to palm keypoints")
    
    parser.add_argument("--sample_radius", type=int, default=0, help="Sample area's height and width")
    parser.add_argument("--tri_kpt_idx", type=list, default=[], help="Targeted points' index in 21 keypoints")
    parser.add_argument("--all_kpt_idx", type=list, default=[], help="All keypoints index in 21 keypoints")
    parser.add_argument("--sample_pits", type=list, default=[], help="Sampling points")
    parser.add_argument("--type", type=str, default="rgb-to-ir", help="Input type")
    return parser


def get_args():
    parser = get_parser()
    return parser.parse_args()

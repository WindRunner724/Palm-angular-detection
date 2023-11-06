import numpy as np
import cv2 as cv
import os

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)


def vis(img, palm_img, angular):
    kpt_idx_7 = [0, 1, 2, 5, 9, 13, 17]
    # plot(img=img, pos_2d=palm_img.kpt_pos_21[kpt_idx_7], pix_val=palm_img.kpt_pix_21[kpt_idx_7], angle=None,
    #      color=BLUE, text_pos=(20, 40))
    plot(img=img, pos_2d=palm_img.kpt_pos_3,             pix_val=palm_img.kpt_pix_3,             angle=angular,
         color=GREEN, text_pos=(40, 40))
    plot_line(img=img, tri_pos_2d=palm_img.kpt_pos_3, color=RED)
    return 0


def merge(img_pair, rtl_img):
    height, width = img_pair.height, img_pair.width
    img = np.zeros((height, width * 3, 3), dtype=np.uint8)
    img[:, 0:width] = img_pair.palm_img
    img[:, width:2 * width] = img_pair.palm_img
    img[:, 2 * width:3 * width] = rtl_img
    return img


def merge_rgb_rtl(args, rgb_img, rtl_img, rtl_name):
    img_rtl = np.hstack((rgb_img, rtl_img))
    cv.imwrite(os.path.join(args.output_images_path, rtl_name), img_rtl)
    return 0


def overly_rgb_ir(args, rgb_img, ir_img, rtl_name):
    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])

    img_rtl = cv.filter2D(rgb_img, -1, kernel)
    cv.imwrite(os.path.join(args.output_images_path + "overly/", rtl_name), img_rtl + ir_img)
    return 0


def plot(img, pos_2d, pix_val, angle, color, text_pos):
    missed_points = []
    for i, position in enumerate(pos_2d):
        if position is None or pix_val[i] is None:
            missed_points.append(i)
            continue

        x = int(position[0])
        y = int(position[1])
        cv.putText(img, str(int(pix_val[i])), (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, )
        #cv.putText(img, str(i), (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, )

    if len(missed_points) != 0:
        text = f"missed points: {str(missed_points)}"
        cv.putText(img, text, text_pos, cv.FONT_HERSHEY_SIMPLEX, 0.5, color, )

    if angle is not None:
        if np.isnan(angle[0]) or np.isnan(angle[1]):
            return
        cv.putText(img, f"left_to_right: {str(int(angle[0]))}", (20, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, GREEN, )
        cv.putText(img, f"top_to_bottom: {str(int(angle[1]))}", (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.5, GREEN, )

    return


def plot_line(img, tri_pos_2d, color):
    if any(pos is None for pos in tri_pos_2d):
        return
    cv.line(img, (int(tri_pos_2d[0][0]), int(tri_pos_2d[0][1])), (int(tri_pos_2d[1][0]), int(tri_pos_2d[1][1])), color,
            2)
    cv.line(img, (int(tri_pos_2d[1][0]), int(tri_pos_2d[1][1])), (int(tri_pos_2d[2][0]), int(tri_pos_2d[2][1])), color,
            2)
    cv.line(img, (int(tri_pos_2d[2][0]), int(tri_pos_2d[2][1])), (int(tri_pos_2d[0][0]), int(tri_pos_2d[0][1])), color,
            2)

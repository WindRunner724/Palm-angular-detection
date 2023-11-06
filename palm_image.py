import cv2 as cv
import os
import numpy as np


def vec_shift(a, b, c):
    vec1 = c - a
    vec2 = (c - b) / 2
    vec = vec1 - vec2
    return vec / 3


class PalmImg:

    def __init__(self, args, palm_path, index, sample_radius):
        self.args = args
        self.palm_path = palm_path
        self.index = index
        self.sample_radius = sample_radius
        self.palm_img = self.load_images(prefix="Ir", file=palm_path)

        self.height, self.width, _ = self.palm_img.shape
        self.kpt_pos_21 = None
        self.kpt_pos_3 = None
        self.kpt_pix_21 = None
        self.kpt_pix_3 = None

    def load_images(self, prefix, file):
        img = cv.imread(os.path.join(self.args.input_images_path, f"{prefix}/{file}"))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        return img

    def set_kpt_21_pos(self, kpt_21):
        self.kpt_pos_21 = kpt_21
        for idx in range(21):
            self.kpt_pos_21[idx, 0] = self.kpt_pos_21[idx, 0] * self.width
            self.kpt_pos_21[idx, 1] = self.kpt_pos_21[idx, 1] * self.height

    # Sample method returns three points' 2D position
    def sample_v1(self):
        # Take midpoint between 5 and 6, between 3 and 4
        # Lower point 0
        c = (self.kpt_pos_21[self.args.all_kpt_idx[5]] + self.kpt_pos_21[self.args.all_kpt_idx[6]]) / 2
        b = (self.kpt_pos_21[self.args.all_kpt_idx[3]] + self.kpt_pos_21[self.args.all_kpt_idx[4]]) / 2
        a = self.kpt_pos_21[0] + vec_shift(self.kpt_pos_21[0], b, c)
        self.kpt_pos_3 = [a, b, c]
        return

    def set_kpt_21_pix(self):
        self.kpt_pix_21 = self.calc_avg_pix(self.kpt_pos_21)
        return

    def set_kpt_3_pix(self):
        self.kpt_pix_3 = self.calc_avg_pix(self.kpt_pos_3)
        return

    def calc_avg_pix(self, pos_2d):
        pix_avg = []
        for pos in pos_2d:
            if pos is None or np.isnan(pos[0]) or np.isnan(pos[1]):
                pix_avg.append(None)
                continue
            left = int(pos[1]) - self.sample_radius
            right = int(pos[1]) + self.sample_radius
            top = int(pos[0]) + self.sample_radius
            bottom = int(pos[0]) - self.sample_radius
            if left < 0:
                left = 0
            if right >= 988:
                right = 988
            if bottom < 0:
                bottom = 0
            if top >= 720:
                top = 720

            if left == right | bottom == top:
                pix_avg.append(None)
                continue

            img_sub = self.palm_img[left:right, bottom:top]
            indices = np.where(img_sub != 0)
            if len(img_sub[indices]) == 0:
                pix_avg.append(0)
            else:
                pix_avg.append(np.average(img_sub[indices]))

        return np.array(pix_avg)

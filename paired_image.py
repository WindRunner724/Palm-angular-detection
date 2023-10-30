import cv2 as cv
import os
import numpy as np


def vec_shift(a, b, c):
    vec1 = c - a
    vec2 = (c - b) / 2
    vec = vec1 - vec2
    return vec / 3


class PairedImg:

    def __init__(self, args, rgb_path, ir_path, index, hands, sample_radius):
        self.args = args
        self.rgb_path = rgb_path
        self.ir_path = ir_path
        self.index = index
        self.hands = hands
        self.sample_radius = sample_radius
        self.rgb_img = self.load_images(prefix="rgb", file=rgb_path)
        self.ir_img = self.load_images(prefix="ir", file=ir_path)

        self.height, self.width, _ = self.rgb_img.shape
        self.kpt_pos_21 = None
        self.kpt_pos_3 = None
        self.kpt_pix_21 = None
        self.kpt_pix_3 = None

    def load_images(self, prefix, file):
        img = cv.imread(os.path.join(self.args.input_images_path, f"{prefix}/{file}"))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        return img

    def kpt_estimation(self, detected_img):
        if detected_img == "RGB":
            detected_img = self.rgb_img
        elif detected_img == "IR":
            detected_img = self.ir_img
        else:
            raise ValueError('Keypoints estimation object images type error. Please type RGB or IR')

        rtl = self.hands.process(detected_img).multi_hand_landmarks
        if rtl:
            pos_3d = np.array([[rtl[0].landmark[i].x, rtl[0].landmark[i].y, rtl[0].landmark[i].z]
                               for i in range(len(rtl[0].landmark))])
            mask = (pos_3d[:, 0] >= 0) & (pos_3d[:, 0] <= 1) & (pos_3d[:, 1] >= 0) & (pos_3d[:, 1] <= 1)
            pos_3d[~mask] = None
            self.kpt_pos_21 = np.array([[point[0] * self.width, point[1] * self.height] for point in pos_3d])
            return True
        else:
            return False

    # Sample method returns three points' 2D position
    def sample_v1(self):
        # Take midpoint between 5 and 6, between 3 and 4
        # Lower point 0
        c = (self.kpt_pos_21[self.args.all_kpt_idx[5]] + self.kpt_pos_21[self.args.all_kpt_idx[6]]) / 2
        b = (self.kpt_pos_21[self.args.all_kpt_idx[3]] + self.kpt_pos_21[self.args.all_kpt_idx[4]]) / 2
        a = self.kpt_pos_21[0] + vec_shift(self.kpt_pos_21[0], b, c)
        self.kpt_pos_3 = [a, b, c]
        return

    def set_kpt_21(self):
        self.kpt_pix_21 = self.calc_avg_pix(self.kpt_pos_21)
        return

    def set_kpt_3(self):
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

            img_sub = self.ir_img[left:right, bottom:top]
            indices = np.where(img_sub != 0)
            if len(img_sub[indices]) == 0:
                pix_avg.append(0)
            else:
                pix_avg.append(np.average(img_sub[indices]))

        return np.array(pix_avg)

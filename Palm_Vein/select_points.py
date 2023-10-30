from math import ceil, floor
import numpy as np


def point_0(size, width=1, ):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    for i in range(0, size):
        y = i + 1
        for x in range(center - t, center + t + 1):
            point_list.append((x, y))
    return point_list


def point_15(size, width=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    k, r = divmod(center - 2, 4)
    for i in range(k):
        x = center - i - 1
        for x in range(x - t, x + t + 1):
            point_list.extend([(x, center + 1 + 4 * i + 1), (x, center + 1 + 4 * i + 2), (x, center + 1 + 4 * i + 3),
                               (x, center + 1 + i * 4 + 4)])
        x = center + i + 1
        for x in range(x - t, x + t + 1):
            point_list.extend([(x, center - 1 - i * 4 - 1), (x, center - 1 - i * 4 - 2), (x, center - 1 - i * 4 - 3),
                               (x, center - 1 - i * 4 - 4)])
    if r != 0:
        for j in range(1, r + 1):
            x = center - (k + 1)
            for x in range(x - t, x + t + 1):
                y = center + 1 + k * 4 + j
                point_list.extend([(x, y)])
            x = center + (k + 1)
            for x in range(x - t, x + t + 1):
                y = center - 1 - k * 4 - j
                point_list.extend([(x, y)])
    x = center
    for x in range(x - t, x + t + 1):
        point_list.extend([(x, center), (x, center - 1), (x, center + 1), ])
    # return sorted(point_list, reverse=True)
    return point_list


def point_30(size, width=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    k, r = divmod(center - 1, 2)
    for i in range(1, k + 1):
        x = center + i
        for x in range(x - t, x + t + 1):
            point_list.extend([(x, center - (2 * i - 1)), (x, center - 2 * i)])
        x = center - i
        for x in range(x - t, x + t + 1):
            point_list.extend([(x, center + (2 * i - 1)), (x, center + 2 * i)])
    if r == 1:
        x = center + k + 1
        for x in range(x - t, x + t + 1):
            y = center - (2 * k + 1)
            point_list.append((x, y))
        x = center - (k + 1)
        for x in range(x - t, x + t + 1):
            y = center + (2 * k + 1)
            point_list.append((x, y))
    x = center
    for x in range(x - t, x + t + 1):
        point_list.append((x, center))
    # point_list.sort(reverse=True)
    return sorted(point_list, reverse=True)


def point_45(size, width=1):
    point_list = []
    center = ceil(size / 2)
    # print(center)
    t = floor(width / 2)
    # print(t)
    for i in range(1, center):
        x = center + i
        y = center - i
        for y in range(y - t, y + t + 1):
            if y >= 1:
                point_list.append((x, y))
        x = center - i
        y = center + i
        for y in range(y - t, y + t + 1):
            if y <= size:
                point_list.append((x, y))
    x = center
    y = center
    for y in range(y - t, y + t + 1):
        point_list.append((x, y))

    t = ceil(width / 2)
    for i in range(t, 0, -1):
        for j in range(size - width + 1, size - width + i):
            point_list.append((t - i + 1, j))

    for i in range(0, t - 1):
        for j in range(t + i + 1, width + 1):
            point_list.append((size - i, j))
    return sorted(point_list, reverse=True)


def point_60(size, width=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    k, r = divmod(center - 1, 2)
    for i in range(1, k + 1):
        y = center + i
        for y in range(y - t, y + t + 1):
            point_list.extend([(center - (2 * i - 1), y), (center - 2 * i, y)])
        y = center - i
        for y in range(y - t, y + t + 1):
            point_list.extend([(center + (2 * i - 1), y), (center + 2 * i, y)])
    if r == 1:
        y = center + k + 1
        for y in range(y - t, y + t + 1):
            x = center - (2 * k + 1)
            point_list.append((x, y))
        y = center - (k + 1)
        for y in range(y - t, y + t + 1):
            x = center + (2 * k + 1)
            point_list.append((x, y))
    y = center
    for y in range(y - t, y + t + 1):
        point_list.append((center, y))
    # point_list.sort(reverse=True)
    return sorted(point_list, reverse=True)


def point_75(size, width=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    k, r = divmod(center - 2, 4)
    for i in range(k):
        y = center - i - 1
        for y in range(y - t, y + t + 1):
            point_list.extend([(center + 1 + 4 * i + 1, y), (center + 1 + 4 * i + 2, y), (center + 1 + 4 * i + 3, y),
                               (center + 1 + i * 4 + 4, y)])
        y = center + i + 1
        for y in range(y - t, y + t + 1):
            point_list.extend([(center - 1 - i * 4 - 1, y), (center - 1 - i * 4 - 2, y), (center - 1 - i * 4 - 3, y),
                               (center - 1 - i * 4 - 4, y)])
    if r != 0:
        for j in range(1, r + 1):
            y = center - (k + 1)
            for y in range(y - t, y + t + 1):
                x = center + 1 + k * 4 + j
                point_list.extend([(x, y)])
            y = center + (k + 1)
            for y in range(y - t, y + t + 1):
                x = center - 1 - k * 4 - j
                point_list.extend([(x, y)])
    y = center
    for y in range(y - t, y + t + 1):
        point_list.extend([(center, y), (center - 1, y), (center + 1, y), ])
    return sorted(point_list, reverse=True)


def point_90(size, width=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    for i in range(1, size + 1):
        x = i
        for y in range(center - t, center + t + 1):
            point_list.append((x, y))
    return point_list


def point_105(size, width=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    k, r = divmod(center - 2, 4)
    for i in range(k):
        y = center + i + 1
        for y in range(y - t, y + t + 1):
            point_list.extend([(center + 1 + 4 * i + 1, y), (center + 1 + 4 * i + 2, y), (center + 1 + 4 * i + 3, y),
                               (center + 1 + i * 4 + 4, y)])
        y = center - i - 1
        for y in range(y - t, y + t + 1):
            point_list.extend([(center - 1 - i * 4 - 1, y), (center - 1 - i * 4 - 2, y), (center - 1 - i * 4 - 3, y),
                               (center - 1 - i * 4 - 4, y)])
    if r != 0:
        for j in range(1, r + 1):
            y = center + (k + 1)
            for y in range(y - t, y + t + 1):
                x = center + 1 + k * 4 + j
                point_list.extend([(x, y)])
            y = center - (k + 1)
            for y in range(y - t, y + t + 1):
                x = center - 1 - k * 4 - j
                point_list.extend([(x, y)])
    y = center
    for y in range(y - t, y + t + 1):
        point_list.extend([(center, y), (center - 1, y), (center + 1, y)])
    return sorted(point_list, reverse=True)


def point_120(size, width=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    k, r = divmod(center - 1, 2)
    for i in range(1, k + 1):
        y = center + i
        for y in range(y - t, y + t + 1):
            point_list.extend([(center + (2 * i - 1), y), (center + 2 * i, y)])
        y = center - i
        for y in range(y - t, y + t + 1):
            point_list.extend([(center - (2 * i - 1), y), (center - 2 * i, y)])
    if r == 1:
        y = center + k + 1
        for y in range(y - t, y + t + 1):
            x = center + (2 * k + 1)
            point_list.append((x, y))
        y = center - (k + 1)
        for y in range(y - t, y + t + 1):
            x = center - (2 * k + 1)
            point_list.append((x, y))
    y = center
    for y in range(y - t, y + t + 1):
        point_list.append((center, y))
    return sorted(point_list, reverse=True)


def point_135(size, width=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    for i in range(1, center):
        x = center - i
        y = center - i
        for y in range(y - t, y + t + 1):
            if y >= 1:
                point_list.append((x, y))
        x = center + i
        y = center + i
        for y in range(y - t, y + t + 1):
            if y <= size:
                point_list.append((x, y))
    x = center
    y = center
    for y in range(y - t, y + t + 1):
        point_list.append((x, y))

    for i in range(0, t):
        for j in range(1, t - i + 1):
            point_list.append((width - i, j))
    for i in range(0, t):
        for j in range(1, t - i + 1):
            # point_list.append((size - i, size - width + j))
            point_list.append((size - width + j, size - i))
    return sorted(point_list, reverse=True)


def point_150(size, width):
    point_list = []
    center = ceil(size / 2)
    t = floor(width / 2)
    # print(center)
    k, r = divmod(center - 1, 2)
    for i in range(1, k + 1):
        x = center + i
        for x in range(x - t, x + t + 1):
            point_list.extend([(x, center + (2 * i - 1)), (x, center + 2 * i)])
        x = center - i
        for x in range(x - t, x + t + 1):
            point_list.extend([(x, center - (2 * i - 1)), (x, center - 2 * i)])
    if r == 1:
        x = center + k + 1
        for x in range(x - t, x + t + 1):
            y = center + (2 * k + 1)
            point_list.append((x, y))
        x = center - (k + 1)
        for x in range(x - t, x + t + 1):
            y = center - (2 * k + 1)
            point_list.append((x, y))
    x = center
    for x in range(x - t, x + t + 1):
        point_list.append((x, center))
    # point_list.sort(reverse=True)
    return sorted(point_list, reverse=True)


def point_165(size, wide=1):
    point_list = []
    center = ceil(size / 2)
    t = floor(wide / 2)
    # print(center)
    k, r = divmod(center - 2, 4)
    for i in range(k):
        x = center + i + 1
        for x in range(x - t, x + t + 1):
            point_list.extend([(x, center + 1 + 4 * i + 1), (x, center + 1 + 4 * i + 2), (x, center + 1 + 4 * i + 3),
                               (x, center + 1 + i * 4 + 4)])
        x = center - i - 1
        for x in range(x - t, x + t + 1):
            point_list.extend([(x, center - 1 - i * 4 - 1), (x, center - 1 - i * 4 - 2), (x, center - 1 - i * 4 - 3),
                               (x, center - 1 - i * 4 - 4)])
    if r != 0:
        for j in range(1, r + 1):
            x = center + (k + 1)
            for x in range(x - t, x + t + 1):
                y = center + 1 + k * 4 + j
                point_list.extend([(x, y)])
            x = center - (k + 1)
            for x in range(x - t, x + t + 1):
                y = center - 1 - k * 4 - j
                point_list.extend([(x, y)])
    x = center
    for x in range(x - t, x + t + 1):
        point_list.extend([(x, center), (x, center - 1), (x, center + 1), ])
    # return sorted(point_list, reverse=True)
    return point_list


def display_point(filter_ize, points_list):
    point_metric = np.zeros((filter_ize, filter_ize), dtype=np.uint8)
    for point in points_list:
        x, y = point
        point_metric[x - 1, y - 1] = 1
    return point_metric


def points_metric(filter_size, width, angel):
    point_lists = eval("point_" + str(angel) + "(filter_size, width)")
    point_metric = np.zeros((filter_size, filter_size), dtype=np.uint8)
    for point in point_lists:
        x, y = point
        point_metric[x - 1, y - 1] = 1
    return point_metric


def get_filters(filter_size, width=1):
    filters = np.zeros((12, filter_size, filter_size))
    i = 0
    for angel in [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165]:
        filters[i] = points_metric(filter_size, width, angel)
        i += 1
    return filters


def get_filter_str(filter_size, width=1):
    filter_str = []
    for angel in [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165]:
        temp = points_metric(filter_size, width, angel)
        count = 0
        temp_str = ""
        for x in range(filter_size):
            for y in range(filter_size):
                if temp[x, y] == 1:
                    if count == (filter_size - 1):
                        # print(f"f[{x}, {y}]", end=" ")
                        temp_str += f"f[{x}, {y}] "
                        continue
                    temp_str += f"f[{x}, {y}] + "
                    # print(f"f[{x}, {y}] +", end=" ")
                    count += 1
        print()
        print(temp_str)
        filter_str.append(temp_str)
        return filter_str


if __name__ == '__main__':
    r_size = 11
    wid = 1
    print(get_filters(9))
    # filter_str = []
    # for angel in [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165]:
    #     temp = points_metric(r_size, wid, angel)
    #     print(temp)
    #     count = 0
    #     temp_str = ""
    #     for x in range(r_size):
    #         for y in range(r_size):
    #             if temp[x, y] == 1:
    #                 if count == (r_size-1):
    #                     # print(f"f[{x}, {y}]", end=" ")
    #                     temp_str += f"f[{x}, {y}] "
    #                     continue
    #                 temp_str += f"f[{x}, {y}] + "
    #                 # print(f"f[{x}, {y}] +", end=" ")
    #                 count += 1
    #     print()
    #     print(temp_str)
    #     filter_str.append(temp_str)

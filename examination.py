import os


def exam_id_corr(rgb_list, ir_list):
    id_r, id_i = 0, 0
    while id_r < len(rgb_list) & id_i < len(ir_list):
        if rgb_list[id_r][4] < ir_list[id_i][3]:
            del rgb_list[id_r]
        elif rgb_list[id_r][4] > ir_list[id_i][3]:
            del ir_list[id_i]
        else:
            id_r += 1
            id_i += 1

    return len(rgb_list) if len(rgb_list) < len(ir_list) else len(ir_list)


def exam_pix_corr():
    return 0

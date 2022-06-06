import numpy as np


def dilate(image: np.ndarray, structuring_element: np.ndarray) -> np.ndarray:
    result_matrix = np.ndarray(shape=image.shape, dtype=int)
    se_shape = structuring_element.shape
    se_center = tuple(x // 2 for x in se_shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            se_i_begin = max(0, se_center[0] - i)
            se_j_begin = max(0, se_center[1] - j)
            se_i_end = min(se_shape[0], se_center[0] + (image.shape[0] - i))
            se_j_end = min(se_shape[1], se_center[1] + (image.shape[1] - j))
            img_i_begin = max(0, i - (structuring_element.shape[0] - se_center[0]) + 1)
            img_j_begin = max(0, j - (structuring_element.shape[1] - se_center[1]) + 1)
            img_i_end = min(image.shape[0], i + structuring_element.shape[0] - se_center[0])
            img_j_end = min(image.shape[1], j + structuring_element.shape[1] - se_center[1])
            result_matrix[i, j] = int(np.sometrue(
                np.logical_and(image[img_i_begin:img_i_end, img_j_begin:img_j_end],
                               structuring_element[se_i_begin:se_i_end, se_j_begin: se_j_end])))
    return result_matrix


def get_new_pixel_color(structuring_element, img_cut):
    for y in range(structuring_element.shape[0]):
        for z in range(structuring_element.shape[1]):
            if structuring_element[y, z] == 1 and img_cut[y, z] == 0:
                return 0
    return 1


def erode(image: np.ndarray, structuring_element: np.ndarray) -> np.ndarray:
    result_matrix = np.zeros(shape=image.shape, dtype=int)
    se_shape = structuring_element.shape
    se_center = tuple(x // 2 for x in se_shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (i >= se_shape[0] - se_center[0] - 1) and (i + se_shape[0] - se_center[0] - 1 < image.shape[0]) \
                    and (j >= se_shape[1] - se_center[1] - 1) and (j + se_shape[1] - se_center[1] - 1 < image.shape[1]):
                img_i_begin = i - (se_shape[0] - se_center[0] - 1)
                img_j_begin = j - (se_shape[1] - se_center[1] - 1)
                img_i_end = i + (se_shape[0] - se_center[0])
                img_j_end = j + (se_shape[1] - se_center[1])
                img_cut = image[img_i_begin:img_i_end, img_j_begin:img_j_end]
                result_matrix[i, j] = get_new_pixel_color(structuring_element, img_cut)

    return result_matrix

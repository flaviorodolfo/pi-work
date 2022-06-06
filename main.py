import os
import sys
import numpy as np
import time
from load import load_as_ppm


def find_first_filled_col(img, row, col,lastcol):

    if img.data[row, col] == 1:
        while img.data[row, col] == 1 and col > 0:
            col = col - 1
        return col+1
    else:
        while img.data[row, col] == 0 and col < lastcol:
            if img.data[row, col] == 1:
                return col
            col = col + 1
    return -1


def mapping_shapes(img, auximg, i, j, lastimage):
    lastcol = j
    for row in range(i, img.data.shape[0]):
        auxcol = find_first_filled_col(img, row, j, lastcol)
        if auxcol == -1:
            break
        else:
            while img.data[row, auxcol] == 1:
                auximg.data[row, auxcol] = lastimage
                auxcol = auxcol+1
            lastcol = auxcol


def find_shapes(img):
    auximg = np.zeros((img.data.shape[0], img.data.shape[1]), int)
    lastimage = 2
    for i in range(img.data.shape[0]):
        for j in range(img.data.shape[1]):
            if img.data[i, j] == 1 and auximg.data[i, j]  == 0:
                mapping_shapes(img, auximg, i, j, lastimage)
                lastimage = lastimage+1
    return auximg


def closing(img):
    se = np.ones(shape=(11,11), dtype=int)
    closed = img.dilate(se).erode(se)
    return closed


def count_perf_shapes(img, map):
    aux_map = np.zeros((img.data.shape[0], img.data.shape[1]), int)
    for i in range(img.data.shape[0]):
        for j in range(img.data.shape[1]):
            if img.data[i, j] == 1 and map.data[i, j] != 0:
                aux_map.data[i, j] = map.data[i, j]
    return aux_map


def count_shapes(img):
    print("starting image closing..")
    closed_img = closing(img)
    print("closing ended")
    print("starting shapes search")
    image_map = find_shapes(closed_img)
    print("shapes count ended")
    print("starting image subtraction")
    subtract = closed_img.subtract(img)
    print("image subtraction ended")
    print("counting shapes with holes")
    holes_map = count_perf_shapes(subtract, image_map)
    print('number of shapes: ' + str(image_map.max()-1))
    print('number of shapes without holes: ' + str((image_map.max() - 1) - (len(np.unique(holes_map))-1)))
    print('number of shapes with  holes: ' + str(len(np.unique(holes_map))-1))


if __name__ == '__main__':
    cwd = os.getcwd()
    im = load_as_ppm(cwd+"/images/"+sys.argv[1]+".pbm")
    print("image dimensions: " + str(im.data.shape[1])+"x"+str(im.data.shape[0]))
    init = time.time()
    count_shapes(im)
    end = time.time()
    print('time spent: ' + str(round(end-init,2)) +" secondss")

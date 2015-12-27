import cv2 as cv
import numpy as np
import math
from itertools import product
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import dependence.debug_log as debug
from dependence.spatial_enhancement import show_and_write


def _row_convolusion(img):
  height, width = img.shape[0], img.shape[1]
  blank_img = np.zeros((height, width), np.float)

  for row, col in product(range(0, height), range(0, width - 1, 2)):
    blank_img[row, col // 2] = \
      (img[row, col] + img[row, col + 1]) / 2 ** 0.5
    blank_img[row, width // 2 + col // 2] = \
      (img[row, col] - img[row, col + 1]) / 2 ** 0.5

  return blank_img


def _col_convolusion(img):
  height, width = img.shape[0], img.shape[1]
  blank_img = np.zeros((height, width), np.float)

  for row, col in product(range(0, height - 1, 2), range(0, width)):
    blank_img[row // 2, col] = \
      (img[row, col] + img[row + 1, col]) / 2 ** 0.5
    blank_img[height // 2 + row // 2, col] = \
      (img[row, col] - img[row + 1, col]) / 2 ** 0.5

  return blank_img


if __name__ == '__main__':
  img = cv.imread("images/Fig0809(a).tif", 0)
  img = img.astype(float)
  
  nimg = _row_convolusion(img)
  show_and_write(nimg, "nimg")
  nimg = _col_convolusion(nimg)
  show_and_write(nimg, "nimg")





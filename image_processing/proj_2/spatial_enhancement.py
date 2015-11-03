import cv2 as cv
import numpy as np
import math
import sys
from itertools import product
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt

from numpy.random import normal
gaussian_numbers = normal(size=10)

def show_histogram(img):
  print("show histogram")
  height, width = (img.shape[0], img.shape[1])
  n, bins, patches = plt.hist(img.ravel(), 256, [0,256])
  plt.xlabel('gray level')
  plt.ylabel('number')
  plt.grid(True)
  plt.show()
  return 0


def log_transform(img, c):
  height, width = (img.shape[0], img.shape[1])
  blank_image = np.zeros((height, width, 1), np.uint8)
  tmp_image = np.zeros((height, width))
  show_histogram(img)

  if c == -1:
    max_val = 0

    for row, col in product(range(0, height), range(0, width)):
      gray_val = math.log10(1 + img[row, col])
      if gray_val > max_val:
        max_val = gray_val
      tmp_image[row, col] = math.log10(1 + img[row, col])

    for row, col in product(range(0, height), range(0, width)):
      blank_image[row, col] = tmp_image[row, col] * 255 / max_val

  else:
    for row, col in product(range(0, height), range(0, width)):
      blank_image[row, col] = c * math.log10(1 + img[row, col])
  #blank_image =list(
  #                  map(
  #                    lambda x: x * 255 / (max_val - min_val),
  #                    blank_image.ravel()
  #                  )
  #                 ).reshape(height, width)
  cv.imshow('log res', blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return blank_image


def powerlaw_transform(img, c, gamma):
  height, width = (img.shape[0], img.shape[1])
  blank_image = np.zeros((height, width, 1), np.uint8)

  if c != -1:
    for row, col in product(range(0, height), range(0, width)):
      blank_image[row, col] = c * (img[row, col])**gamma

  else:
    max_val = 0
    tmp_image = np.zeros((height, width))

    for row, col in product(range(0, height), range(0, width)):
      tmp_image[row, col] = (img[row, col])**gamma
      if tmp_image[row, col] > max_val:
        max_val = tmp_image[row, col]

    for row, col in product(range(0, height), range(0, width)):
      blank_image[row, col] = tmp_image[row, col] * 255 / max_val

  cv.imshow('powerlaw res', blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()

  return blank_image


def histogram_equalize(img):
  height, width = (img.shape[0], img.shape[1])
  blank_image = np.zeros((height, width, 1), np.uint8)
  org_hist = [0] * 256
  n = height * width

  for row, col in product(range(0, height), range(0, width)):
    org_hist[ img[row, col] ] += 1
  pdf = list(map(lambda x: x / n, org_hist))
  cdf = list(map(lambda x: sum(pdf[:x+1]), range(0, len(pdf))))

  for row, col in product(range(0, height), range(0, width)):
    blank_image[row, col] = 256 * cdf[ img[row, col] ]

  cv.imshow('input img', img)
  cv.imshow('hist equalize res', blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  show_histogram(img)
  show_histogram(blank_image)

  return blank_image


def _filter_conv(src, mask):
  height, width = (src.shape[0], src.shape[1])
  dst = src.copy()
  border = len(mask) // 2

  for row, col in product(range(border, height - border), range(border, width - border)):
    tmp = 0
    for i, j in product(range(-1, 2), range(-1, 2)):
      tmp += mask[i + 1, j + 1] * src[row + i, col + j]

    if tmp < 0:
      dst[row, col] = 0
    elif tmp > 255:
      dst[row, col] = 255
    else:
      dst[row, col] = tmp

  return dst


def laplacian_enhance(img, n = 3):
  #mask = _get_laplacian_mask(n)
  return _filter_conv(img, lap_mask)


def highboost_filter(img, c, n = 3):
  mask = [0] * (n ** 2)
  mask[(n ** 2) // 2] = 1
  mask = list(zip(*[iter(mask)] * 3))
  mask = np.array(mask)

  return _filter_conv(img, mask + lap_mask)


if __name__ == '__main__':
  # Load an color image in grayscale
  img = cv.imread("images/Fig0308(a)(fractured_spine).tif", 0)

  #log_transform(img, 30)
  #powerlaw_transform(img, -1, 3)
  #histogram_equalize(img)
  #histeq_by_opencv(img)
  #show_histogram(img)


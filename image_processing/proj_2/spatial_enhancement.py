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
  blank_image = np.zeros((height, width, 1), np.float)
  for row, col in product(range(0, height), range(0, width)):
    blank_image[row, col] = c * math.log10(1 + img[row, col])


  return blank_image


def powerlaw_transform(img, c, gamma):
  height, width = (img.shape[0], img.shape[1])
  blank_image = np.zeros((height, width, 1), np.float)

  for row, col in product(range(0, height), range(0, width)):
    blank_image[row, col] = c * (img[row, col])**gamma


  return blank_image


def histogram_equalize(img):
  height, width = (img.shape[0], img.shape[1])
  blank_image = np.zeros((height, width, 1), np.float)
  min_val = int(np.amin(img))
  max_val = int(np.amax(img))
  org_hist = [0] * (max_val - min_val + 1)
  n = height * width

  for row, col in product(range(0, height), range(0, width)):
    org_hist[ int(img[row, col]) ] += 1

  pdf = list(map(lambda x: x / n, org_hist))
  cdf = list(map(lambda x: sum(pdf[:x+1]), range(0, len(pdf))))

  for row, col in product(range(0, height), range(0, width)):
    blank_image[row, col] = 255 * cdf[ int(img[row, col]) ]


  return blank_image


def _filter_conv(src, mask):
  border = len(mask) // 2
  src = cv.copyMakeBorder(src, border, border, border, border, cv.BORDER_CONSTANT)
  height, width = (src.shape[0], src.shape[1])
  dst = src.copy()

  for row, col in product(range(border, height - border), range(border, width - border)):
    dst[row, col] = 0
    for i, j in product(range(-1, 2), range(-1, 2)):
      dst[row, col] += mask[i + 1, j + 1] * src[row + i, col + j]


  return dst[border: -border][:, border: -border]


def laplacian_filter(img, n = 3):
  print("laplacian enhancement...", end='', flush=True)
  # create laplacian kernel
  lap_mask = np.array(
              ((-1, -1, -1),
              (-1, 8, -1),
              (-1, -1, -1))
             )

  return _filter_conv(img, lap_mask)


def highboost_filter(img, c, n = 3):
  print("high-boost...", end='', flush=True)
  # create high boost kernel
  lap_mask = np.array(
              ((-1, -1, -1),
              (-1, 8, -1),
              (-1, -1, -1))
             )
  mask = [0] * (n ** 2)
  mask[(n ** 2) // 2] = 1
  mask = list(zip(*[iter(mask)] * n))
  mask = np.array(mask)

  return _filter_conv(img, mask + lap_mask)


if __name__ == '__main__':
  # Load an color image in grayscale
  img = cv.imread("images/Fig0308(a)(fractured_spine).tif", 0)
def highboost_filter_pdf(img, k, n = 3):
  print("high-boost...", end='', flush=True)
  border = n // 2
  mask = [1] * (n ** 2)
  mask = list(zip(*[iter(mask)] * n))
  mask = np.array(mask)
  blur_mask = mask / (n ** 2)
  blur_img = _filter_conv(img, blur_mask).astype(int)
  gmask = img - blur_img
  res_img = img + k * gmask

  return res_img

def smooth(img, n=3):
  print("image smoothing...", end='', flush=True)
  # create avg kernel
  mask = np.array([1] * (n ** 2)) / (n ** 2)
  mask = mask.reshape((n, n))
  dst = _filter_conv(img, mask)

  return dst


def sobel_filter(img):
  print("sobel gradient...")
  # create sobel kernel x-axis and y-axis
  mask_x = np.array(
            ((1, 2, 1),
            (0, 0, 0),
            (-1, -2, -1))
           )
  mask_y = np.array(
            ((1, 0, -1),
            (2, 0, -2),
            (1, 0, -1))
           )
  print("[x-axis filter]")
  img_x = _filter_conv(img, mask_x)
  print("[y-axis filter]")
  img_y = _filter_conv(img, mask_y)
  res = ((img_x ** 2) + (img_y ** 2)) ** 0.5

  return res



  #log_transform(img, 30)
  #powerlaw_transform(img, -1, 3)
  #histogram_equalize(img)
  #histeq_by_opencv(img)
  #show_histogram(img)


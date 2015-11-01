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


if __name__ == '__main__':
  # Load an color image in grayscale
  img = cv.imread("images/Fig0308(a)(fractured_spine).tif", 0)

  #log_transform(img, 30)
  #powerlaw_transform(img, -1, 3)
  #histogram_equalize(img)
  #histeq_by_opencv(img)
  #show_histogram(img)
 

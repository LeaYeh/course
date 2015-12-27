import cv2 as cv
import numpy as np
import math
from itertools import product
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import dependence.debug_log as debug
from dependence.spatial_enhancement import show_and_write

# Haar convolusion mask
h0 = (0.7071067811865475, 0.7071067811865475)
h1 = (0.7071067811865475, -0.7071067811865475)

def _up_sampling(img, RoC):
  height, width = img.shape[0], img.shape[1]

  if RoC == 0:
    img = np.insert(img, slice(1, None), 0, axis=0)
    img = np.insert(img, img.shape[0], 0, axis=0)
  else:
    img = np.insert(img, slice(1, None), 0, axis=1)
    img = np.insert(img, img.shape[1], 0, axis=1)

  return img


def _down_sampling(img, RoC):
  height, width = img.shape[0], img.shape[1]

  if RoC == 0:
    blank_img = np.zeros((height // 2, width), np.float)
    blank_img = img[::2]
  else:
    blank_img = np.zeros((height, width // 2), np.float)
    blank_img = img[::, ::2]

  return blank_img


def _convolusion(img, mask, RoC):
  height, width = img.shape[0], img.shape[1]
  blank_img = np.zeros((height, width), np.float)

  if RoC == 0:
    for row, col in product(range(0, height), range(0, width - 1)):
      blank_img[row, col] = img[row, col] * mask[0] + img[row, col + 1] * mask[1]
  else:
    for row, col in product(range(0, height - 1), range(0, width)):
      blank_img[row, col] = img[row, col] * mask[0] + img[row + 1, col] * mask[1]

  return blank_img


# discrete wavelet transform
def dwt(img, level=1):
  height, width = img.shape[0], img.shape[1]

  assert level <= math.log2(height) and level <= math.log2(width), \
    "input level too large"

  for lev in range(0, level):
    resize = 2 ** lev
    fheight, fwidth = img.shape[0] // resize, img.shape[1] // resize
    fetch_img = img[:fheight, :fwidth]

    low_img = _convolusion(fetch_img, h0, 1)
    low_img = _down_sampling(low_img, 0)
    high_img = _convolusion(fetch_img, h1, 1)
    high_img = _down_sampling(high_img, 0)
    fetch_img = np.append(low_img, high_img, axis=0)

    low_img = _convolusion(fetch_img, h0, 0)
    low_img = _down_sampling(low_img, 1)
    high_img = _convolusion(fetch_img, h1, 0)
    high_img = _down_sampling(high_img, 1)
    fetch_img = np.append(low_img, high_img, axis=1)

    img[:fheight, :fwidth] = fetch_img

  return img


# inverse discrete wavelet transform
def idwt(img, level):
  height, width = img.shape[0], img.shape[1]

  for lev in range(level, 0, -1):
    resize = 2 ** (lev - 1)
    fheight, fwidth = img.shape[0] // resize, img.shape[1] // resize
    fetch_img = img[:fheight, :fwidth]

    a = fetch_img[:fheight//2, :fwidth//2]
    dV = fetch_img[:fheight//2, fwidth//2:None]
    dH = fetch_img[fheight//2:None, :fwidth//2]
    dD = fetch_img[fheight//2:None, fwidth//2:None]

    a = _up_sampling(a, 1)
    dV = _up_sampling(dV, 1)
    dH = _up_sampling(dH, 1)
    dD = _up_sampling(dD, 1)
    low_a = _convolusion(a, h0, 0)
    high_dV = _convolusion(dV, h1, 0)
    low_dH = _convolusion(dH, h0, 0)
    high_dD = _convolusion(dD, h1, 0)
    f1 = low_a + high_dV
    f2 = low_dH + high_dD

    f1 = _up_sampling(f1, 0)
    f2 = _up_sampling(f2, 0)
    low_f1 = _convolusion(f1, h0, 1)
    high_f2 = _convolusion(f2, h1, 1)
    img[:fheight, :fwidth] = low_f1 + high_f2

  return img


if __name__ == '__main__':
  img = cv.imread("images/Fig0809(a).tif", 0)
  img = img.astype(float)
 
  # img = dwt(img, 5)
  # show_and_write(img, "img")
  # a = np.arange(8 * 8)
  # a = a.reshape((8, 8))
  img = dwt(img, 1)
  show_and_write(img, "dwt")
  img = idwt(img, 1)
  show_and_write(img, "idwt")
  # nimg = _convolusion(img, h0, 0)
  # nimg = down_sampling(nimg, 0)
  # mimg = _convolusion(img, h1, 0)
  # mimg = down_sampling(mimg, 0)
  # img = np.append(nimg, mimg, axis=1)
  #
  # nimg = _convolusion(img, h0, 1)
  # nimg = down_sampling(nimg, 1)
  # mimg = _convolusion(img, h1, 1)
  # mimg = down_sampling(mimg, 1)
  # img = np.append(nimg, mimg, axis=0)
  #
  # show_and_write(img, "img")

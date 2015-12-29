import cv2 as cv
import numpy as np
import math
from itertools import product
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
import dependence.debug_log as debug
from dependence.spatial_enhancement import show_and_write

import pywt

coef = 0.5

def formulas_idwt(img, level=1):
  height, width = img.shape

  for lev in range(level, 0, -1):
    resize = 2 ** (lev - 1)
    fheight, fwidth = height // resize, width // resize
    fetch_img = img[:fheight, :fwidth]

    show_and_write(fetch_img, "fetch_img")

    row_even = fetch_img[:fheight//2, ::] + fetch_img[fheight//2:None, ::] 
    row_odd = fetch_img[:fheight//2, ::] - fetch_img[fheight//2:None, ::]
    fetch_img[::2, ::] = row_even
    fetch_img[1::2, ::] = row_odd

    col_even = fetch_img[::, :fwidth//2] + fetch_img[::, fwidth//2:None]
    col_odd = fetch_img[::, :fwidth//2] - fetch_img[::, fwidth//2:None]
    fetch_img[::, ::2] = col_even
    fetch_img[::, 1::2] = col_odd

    img[:fheight, :fwidth] = fetch_img * coef

  return img


def formulas_dwt(img, level=1):
  height, width = img.shape

  for lev in range(0, level):
    resize = 2 ** lev
    fheight, fwidth = height // resize, width // resize
    fetch_img = img[:fheight, :fwidth]

    odd_col = fetch_img[::, 1::2]
    even_col = fetch_img[::, ::2]
    Lc = (even_col + odd_col)
    Hc = (even_col - odd_col)
    fetch_img = np.append(Lc, Hc, axis=1)

    odd_row = fetch_img[1::2, ::]
    even_row = fetch_img[::2, ::]
    Lr = (even_row + odd_row)
    Hr = (even_row - odd_row)
    fetch_img = np.append(Lr, Hr, axis=0)

    img[:fheight, :fwidth] = fetch_img * coef

  return img

if __name__ == '__main__':
  img = cv.imread("images/Fig0809(a).tif", 0)
  img = img.astype(float)

  img = formulas_dwt(img, 7)
  show_and_write(img, "trans")
  img = formulas_idwt(img, 7)
  show_and_write(img, "inv")


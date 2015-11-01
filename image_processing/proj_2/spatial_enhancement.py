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



if __name__ == '__main__':
  # Load an color image in grayscale
  img = cv.imread("images/Fig0308(a)(fractured_spine).tif", 0)

  #log_transform(img, 30)
  #powerlaw_transform(img, -1, 3)
  #histogram_equalize(img)
  #histeq_by_opencv(img)
  #show_histogram(img)
 

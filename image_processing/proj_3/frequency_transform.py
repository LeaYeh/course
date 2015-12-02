from math import e
from math import pi
import dependence.spatial_enhancement as dev
from dependence.spatial_enhancement import cv
from dependence.spatial_enhancement import math
from dependence.spatial_enhancement import plt
from dependence.spatial_enhancement import np
from dependence.spatial_enhancement import matplotlib
from dependence.spatial_enhancement import product


# check if a number is a power of two
def _is_power_2(num):
  return ( num != 0 and ((num & (num - 1)) == 0))

# calc highest bit position then complete to power of 2
def _complete_to_power_2(num):
  return 2 ** (int(math.log(num, 2)) + 1)


# let image be power of 2
def _padding(img):
  height, width = img.shape[0], img.shape[1]
  new_height, new_width = 0, 0

  if not _is_power_2(height):
    new_height = _complete_to_power_2(height)
  if not _is_power_2(width):
    new_width = _complete_to_power_2(width)

  img = np.pad(
          img,
          ((0, new_height - height), (0, new_width - width)),
          'constant', 
          constant_values=0
        )
  
  return img


# implement DFT
def dft():
  return 0


# Fast Fourier Transform
def fft():
  return 0


# High-Frequency-Emphasis Filtering
def hightpass_filter():
  return 0


# Butterworth band reject filter
def butterworth_filter():
  return 0



if __name__ == '__main__':



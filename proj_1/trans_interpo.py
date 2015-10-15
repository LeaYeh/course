import cv2 as cv
import numpy as np
import math
from itertools import product

"ok"
def scale(img, height, width, scale_size):
  new_height = math.ceil(height * scale_size)
  new_width  = math.ceil(width  * scale_size)
  blank_image = np.zeros((new_height, new_width, 1), np.uint8)
  mask = np.zeros((new_height, new_width), np.uint8)
  for col,row in product(range(0, width), range(0, height)):
    blank_image[row*scale_size, col*scale_size] = img[row, col]
    mask[row*scale_size, col*scale_size] = 255
  # here to do interpolation
  cv.imshow('image',mask)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return 0

"need to find offest"
def rotate(img, height, width, angle):
  #end = [[0, 0], [width-1, height-1], [0, height-1], [width-1, 0]]
  theta = angle / 180 * math.pi
  vcos = math.cos(theta)
  vsin = math.sin(theta)
  """
  for point in end:
    point[1] = math.ceil(point[0]*vcos - point[1]*vsin)
    point[0] = math.ceil(point[0]*vcos + point[1]*vsin)
  print(end)
  """
  #print("abs(vsin) = {}, abs(vcos) = {}\n".format(abs(vsin), abs(vcos)))
  new_height = round(width*abs(vsin) + height*abs(vcos))
  new_width  = round(height*abs(vsin) + width*abs(vcos))
  #centroid = (height*0.5, width*0.5)
  #offset = [((new_width-1)*0.5)*vsin - ((new_height-1)*0.5)*vcos + ((height-1)*0.5),
  #          -((new_width-1)*0.5)*vcos - ((new_height-1)*0.5)*vsin + ((width-1)*0.5)]
  #print(offset)
  print("new_height = {}, new_width = {}\n".format(new_height, new_width))
  blank_image = np.zeros((new_height, new_width, 1), np.uint8)
  for x,y in product(range(0, width), range(0, height)):
    #x -= centroid[1]
    #y -= centroid[0]
    w = x*vcos - y*vsin #+ offset[0]#+ centroid[1]
    h = x*vsin + y*vcos #+ offset[1]#+ centroid[0]
    #x += centroid[1]
    #y += centroid[0]
    #with open("tmp", "a") as f:
    #  f.write("({}, {}) -> ({}, {})\n".format(y, x, math.floor(h), math.floor(w)))
    blank_image[math.floor(h), math.floor(w)] = img[y, x]
    
  cv.imshow('origin',img)
  cv.imshow('image',blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return 0

"ok"
def translate(img, height, width, trans_row, trans_col):
  blank_image = np.zeros((height, width, 1), np.uint8)
  for col,row in product(range(0, width), range(0, height)):
    tmp_row = trans_row + row
    tmp_col = trans_col + col
    if tmp_row in range(0, height) and tmp_col in range(0,  width):
      blank_image[tmp_row, tmp_col] = img[row, col]
  cv.imshow('image',blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return 0

"ok"
def shear(img, height, width, size):
  new_height = size[0]*width  + height
  new_width  = size[1]*height + width
  blank_image = np.zeros((new_height, new_width, 1), np.uint8)
  for col,row in product(range(0, width), range(0, height)):
    tmp_row = row + size[0]*col
    tmp_col = col + size[1]*row
    blank_image[tmp_row, tmp_col] = img[row, col]
  cv.imshow('image',blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return 0

def nearest_neighbor(img, mask):
  height, width = img.shape
  
  return 0

def bilinear():
  return 0

def bicubic():
  return 0



if __name__ == '__main__':
  # Load an color image in grayscale
  img = cv.imread("images/photo.jpg", 0)
  print(img.shape)
  height, width = img.shape

  #shear(img, height, width, (0.5, 0))
  scale(img, height, width, 2)
  #translate(img, height, width, 30, 30)
  ##rotate(img, height, width, 30)
  #print(img[height-1, width-1])
  """
  cv.imshow('image',img)
  cv.waitKey(0)
  cv.destroyAllWindows()
  """




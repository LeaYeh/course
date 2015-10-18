import cv2 as cv
import numpy as np
import math
from itertools import product

# (scale, rotate, shear) all need to interpolate no matter zoom in or zoom out

"ok"
def scale(img, height, width, scale_size, method):
  new_height = math.ceil(height * scale_size)
  new_width  = math.ceil(width  * scale_size)
  blank_image = np.zeros((new_height, new_width, 1), np.uint8)
  if method is "NEAREST_NEIGHBOR":
    for row,col in product(range(0, new_height), range(0, new_width)):
      blank_image[row, col] = img[round(row/scale_size), round(col/scale_size)]
  elif method is "BILINEAR":
    for row,col in product(range(0, new_height), range(0, new_width)):
      map_org = (row/scale_size, col/scale_size)
      base = (math.floor(map_org[0]), math.floor(map_org[1]))
      bias = (map_org[0]-base[0], map_org[1]-base[1])
      if base[0]+1 < height and base[1]+1 < width:
        left  = img[base[0]  , base[1]]   *    bias[0] + \
                img[base[0]+1, base[1]]   * (1-bias[0])
        right = img[base[0]  , base[1]+1] *    bias[0] + \
                img[base[0]+1, base[1]+1] * (1-bias[0])
        blank_image[row, col] = left*bias[1] + right*(1-bias[1])
      elif base[0]+1 < height and base[1] < width:
        left  = img[base[0]  , base[1]]   *    bias[0] + \
                img[base[0]+1, base[1]]   * (1-bias[0])
        blank_image[row, col] = left
      elif base[1]+1 < width and base[0] < height:
        top = img[base[0], base[1]]   *    bias[0] + \
              img[base[0], base[1]+1] * (1-bias[0])
        blank_image[row, col] = top
      #else:
      #boundary still be a problem
  #elif method is "BICUBIC":
    
  """
  for col,row in product(range(0, width), range(0, height)):
    blank_image[row*scale_size, col*scale_size] = img[row, col]
  """
  # here to do interpolation
  cv.imshow('image', blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return 0
def get_rotate_point(point, angle):
  theta = angle / 180 * math.pi
  vcos = math.cos(theta)
  vsin = math.sin(theta)
  return (point[0]*vcos - point[1]*vsin, point[0]*vsin + point[1]*vcos)

"need to find offset"
def get_offset(height, width, angle):
  left_top   = (0, 0)
  left_down  = get_rotate_point((height, 0), angle)
  right_top  = get_rotate_point((0, width), angle)
  right_down = get_rotate_point((height, width), angle)
  print([left_top, left_down, right_top, right_down])
  row_min = math.floor(min([left_top, left_down, right_top, right_down], 
                  key=lambda x: x[0])[0])
  col_min = math.floor(min([left_top, left_down, right_top, right_down], 
                  key=lambda x: x[1])[1])
  return row_min, col_min

def _get_weight(bias):
  bias = abs(bias)
  weights = []
  for i in range(1, -3, -1):
    tmp_bias = abs(bias+i)
    if tmp_bias >= 0 and tmp_bias < 1:
      weights.append(1 - 2*(tmp_bias**2) + (tmp_bias**3))
    elif tmp_bias >= 1 and tmp_bias < 2:
      weights.append(4 - 8*tmp_bias + 5*(tmp_bias**2) - (tmp_bias**3))
    else:
      weights.append(0)
  #with open("weight", "a") as f:
  #  f.write("{}, {}, {}, {}\n".format(weights[0], weights[1], weights[2], weights[3]))
  return weights
  #return [-0.14699999999999935, 0.8470000000000001, 0.36300000000000004, -0.06299999999999972]

def bicubic(img, row, col, angle):

  map_point = get_rotate_point((row, col), -angle)
  base = (math.floor(map_point[0]), math.floor(map_point[1]))
  bias = (map_point[0]-base[0], map_point[1]-base[1])
  wu = _get_weight(bias[0])
  wv = _get_weight(bias[1])
  val = 0
  for cj in range(-1, 3):
    v_value = 0
    for ri in range(-1, 3):
      if _is_in_boundary((base[0]+ri, base[1]+cj), height, width):
        v_value += wu[ri+1] * img[base[0]+ri, base[1]+cj]
      else:
        return 128
    val += wv[cj+1] * v_value
  if val > 255:
    val = 255
  elif val < 0:
    val = 0
  return val
       
def _is_in_boundary(point, height, width):
  if point[0] < 0 or point[0] >= height:
    return False
  if point[1] < 0 or point[1] >= width:
    return False
  return True

def rotate(img, height, width, angle, method):
  theta = angle / 180 * math.pi
  vcos = math.cos(theta)
  vsin = math.sin(theta)
  
  offset = get_offset(height, width, angle)
  print(offset)
  #offset = (-270, 0)
  new_height = round(width*abs(vsin) + height*abs(vcos))
  new_width  = round(height*abs(vsin) + width*abs(vcos))
  blank_image = np.zeros((new_height, new_width, 1), np.uint8)
  for row,col in product(range(0, new_height), range(0, new_width)):
    if method is "NEAREST_NEIGHBOR":
      map_row = round(get_rotate_point((row, col), -angle))[0]
      map_col = round(get_rotate_point((row, col), -angle))[1]
      if _is_in_boundary((map_row, map_col), height, width):
        blank_image[row, col] = img[map_row, map_col]
      else:
        blank_image[row, col] = 128
    elif method is "BILINEAR":
      map_row = get_rotate_point((row+offset[0], col+offset[1]), -angle)[0]
      map_col = get_rotate_point((row+offset[0], col+offset[1]), -angle)[1]
      base = (math.floor(map_row), math.floor(map_col))
      bias = (map_row-base[0], map_col-base[1])
      if _is_in_boundary((base[0]+1, base[1]+1), height, width):
        left = img[base[0]  , base[1]] *    bias[0] + \
               img[base[0]+1, base[1]] * (1-bias[0])
        right = img[base[0]  , base[1]+1] *    bias[0] + \
                img[base[0]+1, base[1]+1] * (1-bias[0])
        blank_image[row, col] = left*bias[1] + right*(1-bias[1])
      else:
        blank_image[row, col] = 128
      # [bug] boundary
    elif method is "BICUBIC":
      blank_image[row, col] = bicubic(img, row+offset[0], col+offset[1], angle)
      """
      elif base[0]+1 < height and base[1] < width:
        left  = img[base[0]  , base[1]]   *    bias[0] + \
                img[base[0]+1, base[1]]   * (1-bias[0])
        blank_image[row, col] = left
      elif base[1]+1 < width and base[0] < height:
        top = img[base[0], base[1]]   *    bias[0] + \
              img[base[0], base[1]+1] * (1-bias[0])
        blank_image[row, col] = top
      else:
        blank_image[row, col] = 128
      """

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

if __name__ == '__main__':
  # Load an color image in grayscale
  img = cv.imread("images/Fig0236(a)(letter_T).tif", 0)
  print(img.shape)
  height, width = img.shape

  print(_get_weight(0.3))
  #shear(img, height, width, (0.5, 0))
  #scale(img, height, width, 5, "BILINEAR")
  #translate(img, height, width, 30, 30)
  rotate(img, height, width, 30, "BICUBIC")
  #print(img[height-1, width-1])
  """
  cv.imshow('image',img)
  cv.waitKey(0)
  cv.destroyAllWindows()
  """




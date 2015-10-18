import cv2 as cv
import numpy as np
import math
from itertools import product

# get weights by bicubic's formulas
def _get_weight(bias):
  bias = abs(bias)
  weights = []
  for i in range(1, -3, -1):
    tmp_bias = abs(bias + i)
    if tmp_bias >= 0 and tmp_bias < 1:
      weights.append(1 - 2 * (tmp_bias ** 2) + (tmp_bias ** 3))
    elif tmp_bias >= 1 and tmp_bias < 2:
      weights.append(4 - 8 * tmp_bias + 5 * (tmp_bias ** 2) - (tmp_bias ** 3))
    else:
      weights.append(0)
  return weights


# check whether the point in boundary
def _is_in_boundary(point, height, width):
  if point[0] < 0 or point[0] >= height:
    return False
  if point[1] < 0 or point[1] >= width:
    return False
  return True


def _get_rotate_point(point, angle):
  theta = angle / 180 * math.pi
  vcos = math.cos(theta)
  vsin = math.sin(theta)
  return [point[0] * vcos - point[1] * vsin, point[0] * vsin + point[1] * vcos]


# get offset for shift image to centroid
def _get_offset(height, width, angle):
  left_top   = (0, 0)
  left_down  = _get_rotate_point((height, 0), angle)
  right_top  = _get_rotate_point((0, width), angle)
  right_down = _get_rotate_point((height, width), angle)
  row_min = math.floor(
              min(
                [left_top, left_down, right_top, right_down], 
                key=lambda x: x[0]
              )[0]
            )
  col_min = math.floor(
              min(
                [left_top, left_down, right_top, right_down], 
                key=lambda x: x[1]
              )[1]
            )
  return row_min, col_min


# implement nearest neighbor alg.
def nearest_neighbor(img, mrow, mcol):
  height, width = img.shape[0], img.shape[1]
  row, col = round(mrow), round(mcol)
  if _is_in_boundary((row, col), height, width):
    return img[row, col]
  return 128


# implement bilinear alg.
def bilinear(img, mrow, mcol):
  height, width = img.shape[0], img.shape[1]
  base = (math.floor(mrow), math.floor(mcol))
  bias = (mrow-base[0], mcol-base[1])
  if _is_in_boundary((base[0]+1, base[1]+1), height, width):
    left  = img[base[0]  , base[1]]   *    bias[0] + \
            img[base[0]+1, base[1]]   * (1-bias[0])
    right = img[base[0]  , base[1]+1] *    bias[0] + \
            img[base[0]+1, base[1]+1] * (1-bias[0])
    return left*bias[1] + right*(1-bias[1])
  return 128


# implement bicubic alg.
def bicubic(img, row, col):
  height, width = img.shape[0], img.shape[1]
  # base = (i, j)
  base = (math.floor(row), math.floor(col))
  # bias = (u, v)
  bias = (row - base[0], col - base[1])
  # calc S(u) and S(v)
  wu = _get_weight(bias[0])
  wv = _get_weight(bias[1])
  val = 0
  for cj in range(-1, 3):
    v_value = 0
    for ri in range(-1, 3):
      if not _is_in_boundary((base[0] + ri, base[1] + cj), height, width):
        return 128
      v_value += wu[ri + 1] * img[base[0] + ri, base[1] + cj]
    val += wv[cj + 1] * v_value
  if val > 255:
    val = 255
  elif val < 0:
    val = 0
  return val


def scale(img, scale_size, method):
  print("start to scale image ...")
  height, width = (img.shape[0], img.shape[1])
  new_height = math.ceil(height * scale_size)
  new_width  = math.ceil(width  * scale_size)
  blank_image = np.zeros((new_height, new_width, 1), np.uint8)
  for row,col in product(range(0, new_height), range(0, new_width)):
    blank_image[row, col] = FUNC[method](img, row / scale_size, col / scale_size)
  cv.imshow('image', blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return blank_image


# left top (0, 0) = the base point of rotation
# after rotation some pixel will be out of result image,
# so we need shift an offset
def rotate(img, angle, method):
  print("start to rotate image ...")
  height, width = img.shape[0], img.shape[1]
  theta = angle / 180 * math.pi
  vcos = math.cos(theta)
  vsin = math.sin(theta)
  offset = _get_offset(height, width, angle)
  new_height = round(width * abs(vsin) + height * abs(vcos))
  new_width  = round(height * abs(vsin) + width * abs(vcos))
  blank_image = np.zeros((new_height, new_width, 1), np.uint8)
  for row, col in product(range(0, new_height), range(0, new_width)):
    map_point = _get_rotate_point((row + offset[0], col + offset[1]), -angle)
    blank_image[row, col] = FUNC[method](img, map_point[0], map_point[1])
  cv.imshow('image', blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return blank_image


def translate(img, trans_row, trans_col):
  print("start to translate image ...")
  height, width = img.shape[0], img.shape[1]
  # create a blank image as result
  blank_image = np.zeros((height, width, 1), np.uint8)
  # from result img position mapping to org image
  for row, col in product(range(0, height), range(0, width)):
    map_point = (row - trans_row, col - trans_col)
    if _is_in_boundary(map_point, height, width):
      # set value from correspond import position     
      blank_image[row, col] = img[map_point[0], map_point[1]]
    else:
      # if result img position not in org image set value to 128
      blank_image[row, col] = 128
  cv.imshow('image',blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return blank_image


def shear(img, size, method):
  print("start to shear image ...")
  height, width = (img.shape[0], img.shape[1])
  new_height = round(size[0] * width  + height)
  new_width  = round(size[1] * height + width)
  blank_image = np.zeros((new_height, new_width, 1), np.uint8) 
  for row, col in product(range(0, new_height), range(0, new_width)):
    map_point = (round(row - size[0] * col), round(col - size[1] * row))
    blank_image[row, col] = FUNC[method](img, map_point[0], map_point[1])
  cv.imshow('image',blank_image)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return blank_image


FUNC = {"NEAREST_NEIGHBOR": nearest_neighbor, 
        "BILINEAR"        : bilinear, 
        "BICUBIC"         : bicubic}

if __name__ == '__main__':
  # Load an color image in grayscale
  img = cv.imread("images/Fig0236(a)(letter_T).tif", 0)

  new_img = scale(img, 2, "BILINEAR")
  new_img = shear(img, (0.5, 0), "BILINEAR")
  new_img = shear(new_img, (0, 0.5), "NEAREST_NEIGHBOR")
  new_img = rotate(img, 30, "BICUBIC")
  new_img = translate(img, 100, 30)
  
  print("completed and save image!\n")
  cv.imwrite("images/result_trans.tif", new_img)

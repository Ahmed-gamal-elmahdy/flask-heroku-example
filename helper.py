#CieLAB images functions

#Check if pixel is background
import numpy as np


def isBG(pixel):
  sum=np.sum(pixel)
  if sum==0 or sum==765:
    return True
  else:
    return False



#to reach cielab you must go from rgb to xyz
#these conversions are from a website
def convert_from_rgb_to_xyz(pixel):
  var_R = ( pixel[0] / 255 )
  var_G = ( pixel[1] / 255 )
  var_B = ( pixel[2] / 255 )

  if ( var_R > 0.04045 ):
    var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
  else:
    var_R = var_R / 12.92
  if ( var_G > 0.04045 ):
    var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
  else:
    var_G = var_G / 12.92
  if ( var_B > 0.04045 ):
    var_B = ( ( var_B + 0.055 ) / 1.055 )** 2.4
  else:
    var_B = var_B / 12.92

  var_R = var_R * 100
  var_G = var_G * 100
  var_B = var_B * 100

  X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
  Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
  return X,Y



def convert_from_xyz_to_lab(xyz_pixel):
  #these constants are from skimage documentation
  var_X = xyz_pixel[0] / 95.047
  var_Y = xyz_pixel[1] / 100.000

  if ( var_X > 0.008856 ):
     var_X = var_X** ( 1/3 )
  else:
     var_X = ( 7.787 * var_X ) + ( 16 / 116 )
  if ( var_Y > 0.008856 ):
     var_Y = var_Y ** ( 1/3 )
  else:
     var_Y = ( 7.787 * var_Y ) + ( 16 / 116 )

  a = 500 * ( var_X - var_Y )
  return a

def getMean(image):
  list_red=[]
  list_green=[]
  for h in range(image.shape[0]):
    for w in range(image.shape[1]):
      pixel=image[h][w]
      if not isBG(pixel):
        xyzPixel=convert_from_rgb_to_xyz(pixel)
        a=convert_from_xyz_to_lab(xyzPixel)
        if a > 0:
          list_red.append(a)
        else:
          list_green.append(a)
  return (np.mean(list_green),np.mean(list_red))

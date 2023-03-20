# Math functions used in many places throughout the code
# Interpolation functions, etc.

import math

def clamp(value, min, max):
   if (value > max):
      return max
   elif value < min:
      return min
   else:
      return value


def clamp_sigmoid(value):
   # clamps value in range from -1 to 1
   # basically just a modified sigmoid function
   # range is normally 0 to 1, so multiply by 2 and subtract one to get desired rang
   clamped = (2 / (1 + math.exp((-1) * value))) - 1
   return clamped


def clamp_trig(value):
   # clamps value in range from -1 to 1
   # similar to the above function but simpler
   # uses the hyperbolic tangent function
   return math.tanh(value)


def in_range(value, lower_limit, upper_limit):
      if (value >= lower_limit) and (value <= upper_limit):
            return True
      else:
            return False


def interpolation(value):
      # array of value from -1 to 1 with corresponding value -12 to 12
      # think of as a list of points on a graph
      arr = [ \
      [-1,-12],\
      [-.85,-6],\
      [-.6,-4],\
      [-.15,0],\
      [.15,0],\
      [.6,4],\
      [.85,6],\
      [1,12]]

      return interpolation_array(value, arr)
      
def interpolation_array(value, arr):
      # if value is less than the first number in array, which is -1, set to first corresponding value in array, which is -12
      if value <= arr[0][0]:
            return arr[0][1]

      # if value is greater than the last number in array, which is 1, set to last corresponding value in array, which is 12
      if value >= arr[len(arr) - 1][0]: 
            return arr[len(arr) - 1][1]

      # if it is inside the range from -1 to 1, then see which two value in the array it is in between
      # return some random number idk what it is that corresponds to the range the value is 
      for i in range(len(arr) - 1):
            if ((value>=arr[i+0][0]) and (value<=arr[i+1][0])): 
                  return (value-arr[i+0][0])*(arr[i+1][1]-arr[i+0][1])/(arr[i+1][0]-arr[i+0][0])+arr[i+0][1]
      return 0

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
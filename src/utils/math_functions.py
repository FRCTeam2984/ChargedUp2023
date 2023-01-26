# Math functions used in many places throughout the code
# Interpolation functions, etc.

def clamp(value, min, max):
   if (value > max):
      return max
   elif value < min:
      return min
   else:
      return value
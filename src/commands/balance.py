from utils import imutil

class Gyro:
   def __init__(self, _gyro : imutil.Imutil):
      self.gyro = _gyro
      self.drive = None
   
   def balance(self):
      rotation = self.gyro.get_pitch()
      max_rotation = 5
      min_rotation = -5

      if (rotation < min_rotation):
         pass
         # drive forward

      if (rotation > max_rotation):
         pass
         # drive backward
      
from utils import imutil
from commands.drive import Drive


class Gyro:
   def __init__(self, _gyro : imutil.Imutil, _drivetrain: Drive):
      self.gyro = _gyro
      self.drivetrain = _drivetrain
   
   def balance(self):
      rotation = self.gyro.get_pitch()
      max_rotation = 5
      min_rotation = -5

      if (rotation < min_rotation):
         self.drivetrain.set_left_speed(2)
         self.drivetrain.set_right_speed(2)
         # figure out the right way to drive forward in the future

      if (rotation > max_rotation):
         self.drivetrain.set_left_speed(-2)
         self.drivetrain.set_right_speed(-2)
      
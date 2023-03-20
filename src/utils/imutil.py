# IMU code copied from last year
# worked well, so we might as well use it again

from ctre import PigeonIMU
from rev import CANSparkMax

class Imutil(PigeonIMU):
   def __init__(self, _parent_motor : CANSparkMax):
      super().__init__(_parent_motor)

   def get_yaw(self):
      #print(f"yaw = {self.getYawPitchRoll()[0]}")
      return self.getYawPitchRoll()[1][0]

   def test(self):
      return self.getYawPitchRoll()

   def get_pitch(self):
      return self.getYawPitchRoll()[1][1]

   def get_roll(self):
      return self.getYawPitchRoll()[1][2]

   def check_if_working(self):
      if (self.getState() == PigeonIMU.PigeonState.Ready):
         return True
      
      else:
         return False
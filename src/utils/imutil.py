# IMU code copied from last year
# worked well, so we might as well use it again

from ctre import WPI_TalonSRX, PigeonIMU

class Imutil(PigeonIMU):
   def __init__(self, _parent_motor : WPI_TalonSRX):
      super().__init__(_parent_motor)

   def get_yaw(self):
      return self.getYawPitchRoll()[0]

   def get_pitch(self):
      return self.getYawPitchRoll()[1]

   def get_roll(self):
      return self.getYawPitchRoll()[2]
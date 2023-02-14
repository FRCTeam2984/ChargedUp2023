from utils import imutil
from commands.drive import Drive
from ctre import WPI_TalonSRX


class Balance:
   def __init__(self, _gyro : imutil.Imutil, _drivetrain: Drive, _front_additional : WPI_TalonSRX, _back_additional : WPI_TalonSRX):
      self.gyro = _gyro
      self.drivetrain = _drivetrain
      
      self.front_additional = _front_additional
      self.back_additional = _back_additional
   
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


   def lower_front_additional(self):
      self.front_additional.set(2)
      # spin motor in correct direction until limit switch is pressed

   def raise_front_additional(self):
      self.back_additional.set(-2)
      # spin motor in correct direction until top limit switch is pressed

      
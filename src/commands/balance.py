from utils import imutil
from subsystems.drive import Drive
from ctre import WPI_TalonSRX


class Balance:
   def __init__(self, _drivetrain: Drive, _gyro : imutil.Imutil):
      self.gyro = _gyro
      self.drivetrain = _drivetrain
   

      # min and max that our pitch can be while still balancing the charge station
      # numbers below are just a guess, will need to actually test to determine correct values
      self.min_rotation = -5
      self.max_rotation = 5

      self.rotation = 0
   
   def auto_balance(self):
      self.rotation = self.gyro.get_pitch()

      if (self.rotation < self.min_rotation):
         self.drivetrain.arcade_drive(0.2, 0)

      elif (self.rotation > self.max_rotation):
         self.drivetrain.arcade_drive(-0.2, 0)

      else:
         self.drivetrain.stop_drive()

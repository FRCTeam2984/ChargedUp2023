from utils import imutil
from subsystems.drive import Drive
from ctre import WPI_TalonSRX


class Balance:
   def __init__(self, _gyro : imutil.Imutil, _drivetrain: Drive, _front_additional : WPI_TalonSRX, _back_additional : WPI_TalonSRX):
      self.gyro = _gyro
      self.drivetrain = _drivetrain
      
      self.front_additional = _front_additional
      self.back_additional = _back_additional

      # min and max that our pitch can be while still balancing the charge station
      # numbers below are just a guess, will need to actually test to determine correct values
      self.min_rotation = -5
      self.max_rotation = 5

      self.rotation = 0
   
   def balance(self):
      self.rotation = self.gyro.get_pitch()

      if (self.rotation < self.min_rotation):
         self.drivetrain.set_speed(2)

      elif (self.rotation > self.max_rotation):
         self.drivetrain.set_speed(-2)

      else:
         self.drivetrain.stop_drive()


   def lower_front_additional(self):
      self.front_additional.set(2)
      # spin motor in correct direction until limit switch is pressed
      # probably deal with this in the limit switch app thingy idk ask greg he knows what this is

   def raise_front_additional(self):
      self.back_additional.set(-2)
      # spin motor in correct direction until top limit switch is pressed

from wpilib import Timer

from subsystems.drive import Drive
from subsystems.arm import Arm
from commands.balance import Balance
from utils import constants, math_functions

class Autonomous:
   def __init__(self, _drive : Drive, _arm : Arm, _balance : Balance):
      self.drive = _drive
      self.arm = _arm
      self.balance = _balance

      self.timer = Timer()
      self.start_time = 0.0

      # stages of autonomous can change later
      self.AUTO_IDLE = 0
      self.AUTO_PLACING_PIECE = 1
      self.AUTO_TURNING = 2
      self.AUTO_MOVING_OUT_COMMUNITY = 3
      self.AUTO_DONE = 4
      self.auto_stage = self.AUTO_IDLE


   def placing_piece(self):
      return True


   def turning(self):
      current_angle = self.drive.drive_imu.get_yaw()
      desired_angle = current_angle + 180

      self.drive.absolute_drive(0, 0, desired_angle, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)

      if math_functions.in_range(current_angle, desired_angle - 5, desired_angle + 5):
         return True

   def moving_out_community(self):
      self.drive.arcade_drive(0.2, 0)

      if self.start_time + 2 < self.timer.getFPGATimestamp():
         return True


   # should place the cone we load it with, turn 180 degrees, and drive forward for 2.5 seconds out of the community
   def auto_mode_one(self):
      if self.auto_stage == self.AUTO_IDLE:
            # check that we are good to start autonomous
            self.auto_stage = self.AUTO_PLACING_PIECE
         

      elif self.auto_stage == self.AUTO_PLACING_PIECE:
         if self.placing_piece():
            self.auto_stage = self.AUTO_TURNING


      elif self.auto_stage == self.AUTO_TURNING:
         if self.turning():
            self.auto_stage = self.AUTO_MOVING_OUT_COMMUNITY
            self.start_time = self.timer.getFPGATimestamp()


      elif self.auto_stage == self.AUTO_MOVING_OUT_COMMUNITY:
         if self.moving_out_community():
            self.auto_stage = self.AUTO_DONE


      elif self.auto_stage == self.AUTO_DONE:
         pass
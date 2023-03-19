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
      self.AUTO_MOVING_OUT_COMMUNITY = 2
      self.AUTO_PREPARING = 3
      self.AUTO_DONE = 4
      self.auto_stage = self.AUTO_IDLE

      # idle, extending arm, wait for a second, back up 3 seconds at a given speed


   def placing_piece(self):
      self.arm.base_desired_position = 0
      
      #print(f"base (z, p, d) = {self.arm.base_encoder_zero}, {self.arm.base_encoder_zero - self.arm.get_base_motor_encoder()}, {self.arm.base_desired_position}")

      if self.start_time + 3 < self.timer.getFPGATimestamp():
         return True

   """def turning(self):
      current_angle = self.drive.drive_imu.get_yaw()
      desired_angle = current_angle + 180

      self.drive.absolute_drive(0, 0, desired_angle, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)

      if math_functions.in_range(current_angle, desired_angle - 5, desired_angle + 5):
         return True"""

   def moving_out_community(self, drive_imu_init):
      #self.drive.arcade_drive(0, 0.4)
      self.drive.absolute_drive(2, 0, drive_imu_init, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)

      if self.start_time + 3.5 < self.timer.getFPGATimestamp():
         return True

   def preparing(self):
      self.arm.open_cube_arm()

      #print(f"start time = {self.start_time}, current time = {self.timer.getFPGATimestamp()}")
      if self.start_time + 3 < self.timer.getFPGATimestamp():
         return True

   # should place the cone we load it with, turn 180 degrees, and drive forward for 2.5 seconds out of the community
   def auto_mode_one(self, drive_imu_init):
      if self.auto_stage == self.AUTO_IDLE:
            # check that we are good to start autonomous
            self.auto_stage = self.AUTO_PLACING_PIECE
            self.arm.base_encoder_zero = self.arm.get_base_motor_encoder() + 8
            self.start_time = self.timer.getFPGATimestamp()

      elif self.auto_stage == self.AUTO_PLACING_PIECE:
         if self.placing_piece():
            self.auto_stage = self.AUTO_MOVING_OUT_COMMUNITY
            self.start_time = self.timer.getFPGATimestamp()
            print("done placing")

      elif self.auto_stage == self.AUTO_MOVING_OUT_COMMUNITY:
         if self.moving_out_community(drive_imu_init):
            self.auto_stage = self.AUTO_PREPARING
            self.start_time = self.timer.getFPGATimestamp()
            print("done moving")
            self.drive.stop_drive()


      elif self.auto_stage == self.AUTO_PREPARING:
         if self.preparing():
            self.auto_stage = self.AUTO_DONE
            print("done prep")

      elif self.auto_stage == self.AUTO_DONE:
         print("done auto")
         

      self.arm.set_base_position(self.arm.base_desired_position)

from wpilib import Timer, DigitalInput

from subsystems.drive import Drive
from subsystems.arm import Arm
from commands.balance import Balance
from utils import constants, math_functions

class Autonomous:
   def __init__(self, _drive : Drive, _arm : Arm, _balance : Balance, _left_switch : DigitalInput, _right_switch : DigitalInput):
      self.drive = _drive
      self.arm = _arm
      self.balance = _balance

      self.left_switch = _left_switch
      self.right_switch = _right_switch

      self.timer = Timer()
      self.start_time = 0.0

      # stages of autonomous can change later
      self.AUTO_IDLE = 0
      self.AUTO_PLACING_PIECE = 1
      self.AUTO_MOVING_LEFT = 2
      self.AUTO_MOVING_RIGHT = 3
      self.AUTO_MOVING_OUT_COMMUNITY = 4
      self.AUTO_PREPARING = 5
      self.AUTO_DONE = 6
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

   def moving_left(self, drive_imu_init):
      self.drive.absolute_drive(0, -3.5, drive_imu_init, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)

      #print(f"drive_imu_init = {drive_imu_init}, imu yaw = {self.drive.drive_imu.get_yaw()}")

      if self.start_time + 5.5 < self.timer.getFPGATimestamp():
         return True

   def moving_right(self, drive_imu_init):
      self.drive.absolute_drive(0, 3.5, drive_imu_init, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)

      if self.start_time + 5.5 < self.timer.getFPGATimestamp():
         return True


   def moving_out_community(self, drive_imu_init):
      #self.drive.arcade_drive(0, 0.4)
      self.drive.absolute_drive(2, 0, drive_imu_init, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)

      if self.start_time + 3.5 < self.timer.getFPGATimestamp():
         return True

   def preparing(self):
      #print(f"start time = {self.start_time}, current time = {self.timer.getFPGATimestamp()}")
      if self.start_time + 3 < self.timer.getFPGATimestamp():
         return True

   # should place the cone we load it with, turn 180 degrees, and drive forward for 2.5 seconds out of the community
   def autonomous(self, drive_imu_init):
      if self.auto_stage == self.AUTO_IDLE:
            # check that we are good to start autonomous
            self.auto_stage = self.AUTO_PLACING_PIECE
            self.arm.base_encoder_zero = self.arm.get_base_motor_encoder() + 15
            self.start_time = self.timer.getFPGATimestamp()

      elif self.auto_stage == self.AUTO_PLACING_PIECE:
         if self.placing_piece():
            print("done placing")
            # left high right low
            if self.left_switch.get() and not self.right_switch.get():
               self.auto_stage = self.AUTO_MOVING_RIGHT
               print("starting to move right")

            elif not self.left_switch.get() and self.right_switch.get():
               self.auto_stage = self.AUTO_MOVING_LEFT
               print("starting to move left")
            
            elif self.left_switch.get() and self.right_switch.get():
               self.auto_stage = self.AUTO_MOVING_OUT_COMMUNITY
               print("starting to move straight back")


            """elif not self.left_switch.get() and not self.right_switch.get():
               print("not doing anything")
               return -1"""
            

            self.start_time = self.timer.getFPGATimestamp()

      elif self.auto_stage == self.AUTO_MOVING_LEFT:
         if self.moving_left(drive_imu_init):
            self.auto_stage = self.AUTO_MOVING_OUT_COMMUNITY
            self.start_time = self.timer.getFPGATimestamp()
            print("done moving left")
      
      elif self.auto_stage == self.AUTO_MOVING_RIGHT:
         if self.moving_right(drive_imu_init):
            self.auto_stage = self.AUTO_MOVING_OUT_COMMUNITY
            self.start_time = self.timer.getFPGATimestamp()
            print("done moving right")

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

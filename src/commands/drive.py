# Has modes of driving such as arcade drive, tank drive, mecanum drive, etc.
# Those driving modes use the simpler functions that turn motors/drivetrains

from ctre import WPI_TalonFX
from rev import CANSparkMax
from utils import constants, math_functions
import math


class Drive:
   def __init__(self, _frontLeft : WPI_TalonFX, _frontRight : WPI_TalonFX, _middleLeft : CANSparkMax, _middleRight : CANSparkMax, _backLeft : WPI_TalonFX, _backRight : WPI_TalonFX):
      
      # Front and back mecanum wheels are powered Falcon500 motors
      self.front_left = _frontLeft
      self.front_right = _frontRight
      self.back_left = _backLeft
      self.back_right = _backRight

      # Middle omni wheels are powered by Neo550 motors
      self.middle_right = _middleRight
      self.middle_left = _middleLeft

      # Constant wheel speed/voltages
      self.MIDDLE_WHEEL_SPEED = 3


   # set the speed of the wheels on the left of the robot and includes the middle wheels
   def set_left_speed(self, speed):
      # clamp the speed from -1 to 1
      speed = math_functions.clamp(speed, -1, 1)

      self.front_left.set(speed)
      self.back_left.set(speed)
      #self.middle_right.setVoltage(self.MIDDLE_WHEEL_SPEED)


   # set the speed of the wheels on the right of the robot and includes the middle wheels
   def set_right_speed(self, speed):
      # clamp the speed from -1 to 1
      speed = math.functions.clamp(speed, -1, 1)

      self.front_right.set(speed)
      self.back_right.set(speed)
      #self.middle_right.setVoltage(self.MIDDLE_WHEEL_SPEED)


   def set_speed(self, speed):
      self.set_left_speed(speed)
      self.set_right_speed(speed)

   
   # Actual driving functions
   def arcade_drive(self, x, y):
      pass


   def tank_drive(self, joystick_left, joystick_right):
      self.set_left_speed(joystick_left)
      self.set_right_speed(joystick_right)


   def mecanum_drive(self, joystick_x, joystick_y):
      front_left_speed = joystick_y + joystick_x
      front_right_speed = joystick_y - joystick_x
      back_right_speed = front_left_speed
      back_left_speed = front_right_speed

      steer = 0
      front_left_speed -= steer
      front_right_speed += steer
      back_left_speed -= steer
      back_right_speed += steer

      # set middle wheel speeds to the average speed of the wheels on the respective sides
      # utilizes the additional power that the middle wheels offer without interfering with mecanum drive (hopefully)
      # might need to round down the avg values or set them to zero if they are in a small range close to 0
      middle_left_speed = (front_left_speed + back_left_speed) / 2
      middle_right_speed = (front_right_speed + back_right_speed) / 2

      self.front_left.setSpeed(front_left_speed)
      self.middle_left.setSpeed(middle_left_speed)
      self.back_left.setSpeed(back_left_speed)

      self.front_right.setSpeed(front_right_speed)
      self.middle_right.setSpeed(middle_right_speed)
      self.back_right.setSpeed(back_right_speed)

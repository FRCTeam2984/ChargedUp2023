# functions for moving joints and servos on the arm to make it move in certain ways
# Those functions are used to pick up the cones/cubes and place them where they need to be

from wpilib import Servo
from rev import CANSparkMax

from utils import math_functions

class Arm:
   def __init__(self, _arm_elevator_motor : CANSparkMax, _arm_base_motor : CANSparkMax, _arm_end_servo_1 : Servo, _arm_end_servo_2 : Servo):
      self.arm_elevator_motor = _arm_elevator_motor
      self.arm_base_motor = _arm_base_motor

      self.arm_end_servo_1 = _arm_end_servo_1
      self.arm_end_servo_2 = _arm_end_servo_2


   def set_servo_1_angle(self, angle):
      clamped_angle = math_functions.clamp(angle, 0, 360)
      self.arm_end_servo_1.setAngle(clamped_angle)

   def set_servo_2_angle(self, angle):
      clamped_angle = math_functions.clamped(angle, 0, 360)
      self.arm_end_servo_2.setAngle(clamped_angle)

   def raise_elevator(self, speed):
      clamped_speed = math_functions.clamp(speed, 1, -1)
      self.arm_elevator_motor.set(clamped_speed)

   def lower_elevator(self, speed):
      clamped_speed = math_functions.clamp(speed, 1, -1)
      self.arm_elevator_motor.set(clamped_speed)

   def move_chain(self, speed):
      clamped_speed = math_functions.clamp(speed, -1, 1)
      self.arm_chain_motor.set(clamped_speed)


   def position_home(self):
      pass
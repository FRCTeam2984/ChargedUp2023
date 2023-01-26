# functions for moving joints and servos on the arm to make it move in certain ways
# Those functions are used to pick up the cones/cubes and place them where they need to be

from wpilib import Servo
from rev import CANSparkMax

class Arm:
   def __init__(self, _arm_elevator_motor : CANSparkMax, _arm_chain_motor : CANSparkMax, _arm_end_servo : Servo):
      self.arm_elevator_motor = _arm_elevator_motor
      self.arm_chain_motor = _arm_chain_motor
      self.arm_end_servo = _arm_end_servo


   def setArmServoAngle(self, angle):
      # clamp angle in future to make sure in range
      self.arm_end_servo.setAngle(angle)
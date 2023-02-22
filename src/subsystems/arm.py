# functions for moving joints and servos on the arm to make it move in certain ways
# Those functions are used to pick up the cones/cubes and place them where they need to be

from wpilib import Servo
from rev import CANSparkMax, SparkMaxLimitSwitch

from utils import math_functions, pid
# maybe we need to use PID in arm control to get accurate positions and hold it there

class Arm:
   def __init__(self, _arm_elevator_motor : CANSparkMax, _arm_base_motor : CANSparkMax, _arm_end_servo_cube : Servo, _arm_end_servo_cone : Servo, _arm_elevator_limit_switch : SparkMaxLimitSwitch, _arm_base_limit_switch : SparkMaxLimitSwitch, _pid : pid.PID):
      self.arm_elevator_motor = _arm_elevator_motor
      self.arm_base_motor = _arm_base_motor

      self.arm_end_servo_cube = _arm_end_servo_cube
      self.arm_end_servo_cone = _arm_end_servo_cone

      self.arm_elevator_limit_switch = _arm_elevator_limit_switch
      self.arm_base_limit_switch = _arm_base_limit_switch

      self.pid = _pid

      # we can use PID for the elevator motor control, as we can input a target encoder value and the actual encoder value
      self.ENCODER_MIN = 0
      self.ENCODER_MAX = 999

      self.HOME = 0
      self.GROUND = 1
      self.CUBE_ONE = 2
      self.CONE_ONE = 3
      self.CUBE_TWO = 4
      self.CONE_TWO = 5
      self.position = self.HOME



   # functions to move the servos and motors in the arm given a speed or angle
   def set_servo_cube_angle(self, angle):
      clamped_angle = math_functions.clamp(angle, 0, 360)
      self.arm_end_servo_cube.setAngle(clamped_angle)

   def set_servo_cone_angle(self, angle):
      clamped_angle = math_functions.clamped(angle, 0, 360)
      self.arm_end_servo_cone.setAngle(clamped_angle)

   def reset_servo_angles(self):
      self.set_servo_cube_angle(0)
      self.set_servo_cone_angle(0)

   def set_elevator_speed(self, speed):
      clamped_speed = math_functions.clamp(speed, -1, 1)
      self.arm_elevator_motor.set(clamped_speed)

   def set_base_speed(self, speed):
      clamped_speed = math_functions.clamp(speed, -1, 1)
      self.arm_base_motor.set(clamped_speed)

   def get_elevator_motor_encoder(self):
      return self.arm_elevator_motor.getAbsoluteEncoder()

   def get_base_motor_encoder(self):
      return self.arm_base_motor.getAbsoluteEncoder()




   # moving the 
   def set_elevator_position(self, desired_encoder_value):
      clamped_encoder = math_functions.clamp(desired_encoder_value, self.ENCODER_MIN, self.ENCODER_MAX)
      actual_encoder = self.get_elevator_motor_encoder()

      # can we use steer pid? If so, should we rename the function? If not, how can we change the function to make it work with this scenario?
      error = clamped_encoder - actual_encoder
      adjustment = self.pid.steer_pid(error)

      self.set_elevator_speed(adjustment)


   def set_base_position(self, desired_encoder_value):
      clamped_encoder = math_functions.clamp(desired_encoder_value, self.ENCODER_MIN, self.ENCODER_MAX)
      actual_encoder = self.get_base_motor_encoder()

      # can we use steer pid? If so, should we rename the function? If not, how can we change the function to make it work with this scenario?
      error = clamped_encoder - actual_encoder
      adjustment = self.pid.steer_pid(error)

      self.set_base_speed(adjustment)


   # the different positions the arm needs to be able to travel to
   def position_home(self):
      self.reset_servo_angles()

      self.set_elevator_position(0)
      self.set_base_position(0)

      self.position = self.HOME

   def position_ground(self):
      self.position = self.GROUND
      # ask neal tomorrow, i guess we just need percentages of the height/encoder max value and go from there using the functions i made the hopefully work

   def position_cube_one(self):
      self.position = self.CUBE_ONE

   def position_cube_two(self):
      self.position = self.CUBE_TWO

   def position_cone_one(self):
      self.position = self.CONE_ONE

   def position_cone_two(self):
      self.position = self.CONE_TWO
   
   def calibration(self):
      # move motor down until the bottom limit switch is clicked
      # set the ground position to zero
      # move up one revolution at a time until the top limit switch is clicked
      # justify values to get a percent-based system by dividing the total number of revolutions by itself and multiply by 100
      pass

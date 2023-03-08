# functions for moving joints and servos on the arm to make it move in certain ways
# Those functions are used to pick up the cones/cubes and place them where they need to be

from wpilib import Servo, DigitalInput
from rev import CANSparkMax

from utils import math_functions, pid
# maybe we need to use PID in arm control to get accurate positions and hold it there

class Arm:
   def __init__(self, _arm_elevator_motor : CANSparkMax, _arm_base_motor : CANSparkMax, _arm_end_servo_cube : Servo, _arm_end_servo_cone : Servo, _arm_cube_limit_switch : DigitalInput, _pid : pid.PID):
      self.arm_elevator_motor = _arm_elevator_motor
      self.arm_base_motor = _arm_base_motor

      self.arm_end_servo_cube = _arm_end_servo_cube
      self.arm_cube_limit_switch = _arm_cube_limit_switch
      self.cube_servo_min = 0
      self.cube_servo_max = 135

      self.arm_end_servo_cone = _arm_end_servo_cone
      self.cone_servo_min = 0
      self.cone_servo_max = 75

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
   def open_cube_arm(self):
      self.arm_end_servo_cube.setAngle(self.cube_servo_min)

   def close_cube_arm(self):
      self.arm_end_servo_cube.setAngle(self.cube_servo_max)

   def check_holding_cube(self):
      return self.arm_cube_limit_switch.get()

   def lift_cone_arm(self):
      self.arm_end_servo_cone.setAngle(self.cone_servo_max)

   def lower_cone_arm(self):
      self.arm_end_servo_cone.setAngle(self.cone_servo_min)

   def set_elevator_speed(self, speed):
      clamped_speed = math_functions.clamp(speed, -1, 1)

      if clamped_speed > 0:
         print("raising elevator")
      elif clamped_speed < 0:
         print("lowering elevator")
      
      self.arm_elevator_motor.set(clamped_speed)

   def stop_elevator(self):
      self.arm_elevator_motor.set(0)

   def set_base_speed(self, speed):
      clamped_speed = math_functions.clamp(speed, -1, 1)

      if clamped_speed > 0:
         print("raising arm")
      elif clamped_speed < 0:
         print("lowering arm")

      self.arm_base_motor.set(clamped_speed)

   def stop_base(self):
      self.arm_base_motor.set(0)

   def get_elevator_motor_encoder(self):
      return self.arm_elevator_motor.getAbsoluteEncoder()

   def get_base_motor_encoder(self):
      return self.arm_base_motor.getAbsoluteEncoder()


   # moving the elevator to a "desired" position
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
      self.set_elevator_position(0)
      self.set_base_position(0)

      self.position = self.HOME

   def position_ground(self):
      # ask neal tomorrow, i guess we just need percentages of the height/encoder max value and go from there using the functions i made the hopefully work
      self.set_elevator_position(0)
      
      self.position = self.GROUND


   def position_cube_one(self):
      # i just picked random values and i don't even know if the functions i wrote work
      self.set_elevator_position(500)
      self.set_base_position(500)

      self.position = self.CUBE_ONE

   def position_cube_two(self):
      self.set_elevator_position(self.ENCODER_MAX)
      self.set_elevator_position(self.ENCODER_MAX)

      self.position = self.CUBE_TWO

   def position_cone_one(self):
      self.set_elevator_position(500)
      self.set_elevator_position(500)

      self.position = self.CONE_ONE

   def position_cone_two(self):
      self.set_elevator_position(self.ENCODER_MAX)
      self.set_elevator_position(self.ENCODER_MAX)

      self.position = self.CONE_TWO
   
   def calibration(self):
      # move motor down until the bottom limit switch is clicked
      # set the ground position to zero
      # move up one revolution at a time until the top limit switch is clicked
      # justify values to get a percent-based system by dividing the total number of revolutions by itself and multiply by 100
      self.ENCODER_MAX = 999
      self.ENCODER_MIN = 0

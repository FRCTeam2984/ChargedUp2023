# functions for moving joints and servos on the arm to make it move in certain ways
# Those functions are used to pick up the cones/cubes and place them where they need to be

from wpilib import Servo, DigitalInput
from rev import CANSparkMax, SparkMaxLimitSwitch
from rev._rev import SparkMaxRelativeEncoder

from utils import math_functions, pid
# maybe we need to use PID in arm control to get accurate positions and hold it there

class Arm:
   def __init__(self, _arm_elevator_motor : CANSparkMax, _arm_base_motor : CANSparkMax, _arm_end_servo_cube : Servo, _arm_end_servo_cone : Servo, _arm_cube_limit_switch : DigitalInput, _elevator_pid : pid.PID, _base_pid : pid.PID):
      self.arm_elevator_motor = _arm_elevator_motor
      self.elevator_encoder_zero = 0.12345
      self.elevator_desired_position = 0
      self.elevator_max_limit_switch = self.arm_elevator_motor.getForwardLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)
      self.elevator_encoder = self.arm_elevator_motor.getEncoder(SparkMaxRelativeEncoder.Type.kHallSensor, 42)
      self.elevator_encoder_top = 10
      self.elevator_encoder_bottom = 125
      self.elevator_encoder_tolerance = 2

      self.arm_base_motor = _arm_base_motor
      self.base_encoder_zero = 0.12345
      self.base_desired_position = 0
      self.base_min_limit_switch = self.arm_base_motor.getForwardLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)
      self.base_encoder = self.arm_base_motor.getEncoder(SparkMaxRelativeEncoder.Type.kHallSensor, 42)
      self.base_encoder_in = None
      self.base_encoder_out = None
      self.base_encoder_tolerance = 2


      self.arm_end_servo_cube = _arm_end_servo_cube
      self.arm_cube_limit_switch = _arm_cube_limit_switch
      self.cube_servo_min = 0
      self.cube_servo_max = 135

      self.arm_end_servo_cone = _arm_end_servo_cone
      self.cone_servo_min = 0
      self.cone_servo_max = 75

      self.elevator_pid = _elevator_pid
      self.elevator_pid.set_pid(0.02, 0, 0, 0)

      self.base_pid = _base_pid
      self.base_pid.set_pid(0.01, 0, 0, 0)


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

   def cube_arm_open_limit(self):
      if abs(self.arm_end_servo_cube.getAngle - self.cube_servo_min) < 5:
         return True
      else:
         return False




   def lift_cone_arm(self):
      self.arm_end_servo_cone.setAngle(self.cone_servo_max)

   def lower_cone_arm(self):
      self.arm_end_servo_cone.setAngle(self.cone_servo_min)






   def set_elevator_speed(self, speed):
      clamped_speed = math_functions.clamp(speed, -1, 1)

      """if clamped_speed > 0:
         print("raising elevator")
      elif clamped_speed < 0:
         print("lowering elevator")"""
      
      self.arm_elevator_motor.set(clamped_speed)

   def stop_elevator(self):
      self.arm_elevator_motor.set(0)

   def set_base_speed(self, speed):
      clamped_speed = math_functions.clamp(speed, -1, 1)

      """if clamped_speed > 0:
         print("raising arm")
      elif clamped_speed < 0:
         print("lowering arm")"""

      self.arm_base_motor.set(clamped_speed)

   def stop_base(self):
      self.arm_base_motor.set(0)





   def get_elevator_motor_encoder(self):
      return self.elevator_encoder.getPosition()

   def get_base_motor_encoder(self):
      return self.base_encoder.getPosition()

   # moving the elevator to a "desired" position
   def set_elevator_position(self, desired_encoder_value):
      self.elevator_desired_position = desired_encoder_value
      actual_encoder = -self.get_elevator_motor_encoder() + self.elevator_encoder_zero

      error = desired_encoder_value - actual_encoder
      adjustment = self.elevator_pid.steer_pid(error) * -1
      adjustment = math_functions.clamp(adjustment, -0.1, 0.1)

      print(f"elevator_error = {error}, elevator_adj = {adjustment}")

      self.set_elevator_speed(adjustment)


   def set_base_position(self, desired_encoder_value):
      self.elevator_desired_position = desired_encoder_value
      actual_encoder = self.get_base_motor_encoder() - self.base_encoder_zero

      # can we use steer pid? If so, should we rename the function? If not, how can we change the function to make it work with this scenario?
      error = desired_encoder_value - actual_encoder
      adjustment = self.base_pid.steer_pid(error)
      adjustment = math_functions.clamp(adjustment, -0.1, 0.1)

      self.set_base_speed(adjustment)

   
   def calibrate_elevator(self):
      # if the elevator is not touching the limit switch, move it up
      # if it is touching the limit switch, get the encoder value and set the class variable to that value

      #print(f"elevator_limit_switch_touching = {self.elevator_encoder.get()}")

      if not self.elevator_max_limit_switch.get():
         self.set_elevator_speed(0.1)

      else:
         encoder_limit_switch_value = self.get_elevator_motor_encoder()
         self.elevator_encoder_zero = encoder_limit_switch_value


   def calibrate_base(self):
      #print(f"base_limit_switch_touching = {self.base_encoder.get()}")


      if not self.base_min_limit_switch.get():
         self.set_base_speed(-0.17)

      else:
         base_limit_switch_value = self.get_base_motor_encoder()
         self.base_encoder_zero = base_limit_switch_value






   # the different positions the arm needs to be able to travel to
   def position_home(self):
      self.set_elevator_position(self.elevator_encoder_top)
      #self.set_base_position(self.base_encoder_in)


      if self.check_arm_close():
         self.position = self.HOME
      else:
         return

   def position_ground(self):
      self.set_elevator_position(115)
      self.set_base_position(30)
      
      
      if self.check_arm_close():
         self.position = self.HOME
      else:
         return


   def check_arm_close(self):
      if abs((self.get_elevator_motor_encoder() - self.elevator_encoder_zero) - self.elevator_desired_position) < self.elevator_encoder_tolerance and abs(self.get_base_motor_encoder() - self.base_encoder_zero) < self.base_encoder_tolerance:
         return True
      else:
         return False


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
   

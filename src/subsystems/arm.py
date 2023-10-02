# functions for moving joints and servos on the arm to make it move in certain ways
# Those functions are used to pick up the cones/cubes and place them where they need to be

from wpilib import Servo, DigitalInput
from rev import CANSparkMax, SparkMaxLimitSwitch
from rev._rev import SparkMaxRelativeEncoder
from ctre import WPI_TalonSRX

from utils import math_functions, pid
# maybe we need to use PID in arm control to get accurate positions and hold it there

class Arm:
   def __init__(self, _arm_base_motor : CANSparkMax, _arm_extension_motor : WPI_TalonSRX, _arm_extension_limit_switch : DigitalInput, _base_pid : pid.PID):
      self.arm_base_motor = _arm_base_motor
      self.base_encoder_zero = 0.12345
      self.base_desired_position = 0
      self.base_desired_position_slow = 0
      self.base_min_limit_switch = self.arm_base_motor.getForwardLimitSwitch(SparkMaxLimitSwitch.Type.kNormallyOpen)
      self.base_encoder = self.arm_base_motor.getEncoder(SparkMaxRelativeEncoder.Type.kHallSensor, 42)
      self.base_encoder_in = 30
      self.base_encoder_out = 3
      self.base_encoder_tolerance = 2

      self.base_pid = _base_pid
      self.base_pid.set_pid(0.1, 0.0016, 0.2, 0) 

      self.arm_extension_motor = _arm_extension_motor
      self.arm_extension_limit_switch = _arm_extension_limit_switch

      self.HOME = 0
      self.GROUND = 1
      self.CUBE_ONE = 2
      self.CONE_ONE = 3
      self.CUBE_TWO = 4
      self.CONE_TWO = 5
      self.position = self.HOME


   def set_base_speed(self, speed):
      clamped_speed = math_functions.clamp(speed, -5, 5)
      self.arm_base_motor.set(clamped_speed)

   def stop_base(self):
      self.arm_base_motor.set(0)


   def set_extension_speed(self, speed):      
      clamped_speed = math_functions.clamp(speed, -5, 5)
      self.arm_extension_motor.set(clamped_speed)

   def stop_extension(self):
      self.arm_extension_motor.set(0)

   def set_intake_speed(self, speed):
      self.arm_claw_motor.set(speed)

   def stop_intake(self):
      self.arm_claw_motor.set(0)

   

   def get_base_motor_encoder(self):
      return self.base_encoder.getPosition()

   def set_base_position(self, desired_encoder_value):
      desired_encoder_value = math_functions.clamp(desired_encoder_value, self.base_encoder_out, self.base_encoder_in)

      self.base_desired_position = desired_encoder_value
      actual_encoder = -self.get_base_motor_encoder() + self.base_encoder_zero

      self.base_desired_position_slow += math_functions.clamp(-self.base_desired_position_slow + desired_encoder_value, -30/100, 30/100)
      

      error = self.base_desired_position_slow - actual_encoder
      adjustment = self.base_pid.keep_integral(error) * -1
      adjustment = math_functions.clamp(adjustment, -0.25, 0.25)

      #print(f"base_error = {error}, base_adj = {adjustment}, actual_encoder = {actual_encoder}")

      self.set_base_speed(adjustment)

   def calibrate_base(self):
      #print(f"base_limit_switch_touching = {self.base_encoder.get()}")

      if not self.base_min_limit_switch.get():
         self.set_base_speed(0.17)

      else:
         base_limit_switch_value = self.get_base_motor_encoder()
         self.base_encoder_zero = base_limit_switch_value


   def base_close_enough(self):
      current_position = (self.get_base_motor_encoder() - self.base_encoder_zero) * -1
      result = math_functions.in_range(current_position, self.base_desired_position - self.base_encoder_tolerance, self.base_desired_position + self.base_encoder_tolerance)

      #print(f"base_close_enough = {result}, current_position = {current_position}, desired_position = {self.base_desired_position}")

      return result




   # the different positions the arm needs to be able to travel to
   def position_home(self):
      #self.elevator_desired_position = 5
      self.base_desired_position = 1

      #self.lift_cone_arm()
      #self.open_cube_arm()

      
      if self.base_close_enough():
         self.position = self.HOME
      else:
         return False

   def position_ground(self):
      #self.elevator_desired_position = 115
      self.base_desired_position = 5

      if self.base_close_enough():
         self.position = self.GROUND
      else:
         return


   def position_cube_one(self):
      # i just picked random values and i don't even know if the functions i wrote work
      pass

      self.position = self.CUBE_ONE

   def position_cube_two(self):
      pass

      self.position = self.CUBE_TWO

   def position_cone_one(self):
      pass

      self.position = self.CONE_ONE

   def position_cone_two(self):
      pass

      self.position = self.CONE_TWO
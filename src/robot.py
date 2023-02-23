import wpilib, rev, ctre
import math
from subsystems import arm, drive, networking, rotary_controller

from utils import math_functions, constants, imutil, pid
from commands import balance, cone, cube, autonomous

"""
NOTE:
BRING EXTRA VRM CABLES TO COMPETITION IN CASE OF SATEFY INSPECTION IDK ASK GREG

TO DO FOR ANY MEETING:
- modes of autonomous
- figure out how to find position of arm without limit switch encoder complicated situation
- polish the PID code (mainly the new stuff i wrote to understand it better)
- state machine format for arm positions
- generally, commands for balancing and moving arms, etc.
"""

class MyRobot(wpilib.TimedRobot): 
   def robotInit(self):
      self.timer = wpilib.Timer()

      # Front and back mecanum wheels are powered Falcon500 motors and drive class instance
      self.front_left = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_LEFT)
      self.front_right = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_RIGHT)
      self.back_left = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_LEFT)
      self.back_right = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_RIGHT)

      # Middle omni wheels are powered by Neo550 motors
      self.middle_right = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_RIGHT)
      self.middle_left = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_LEFT)

      self.front_additional = ctre.WPI_TalonSRX(constants.ID_ADDITIONAL_FRONT)
      self.back_additional = ctre.WPI_TalonSRX(constants.ID_ADDITIONAL_BACK)

      # imu and pid stuff to be added below
      # using the middle left motor, even though the middle right one can be used too
      self.drive_imu = imutil.PigeonIMU(self.middle_left)
      self.pid = pid.PID()

      # Motors and servos that control arm
      self.arm_elevator_motor = rev.CANSparkMax(constants.ID_ARM_ELEVATOR)
      self.arm_base_motor = rev.CANSparkMax(constants.ID_ARM_CHAIN)
      self.arm_end_servo_1 = wpilib.Servo(constants.ID_ARM_SERVO_1)
      self.arm_end_servo_2 = wpilib.Servo(constants.ID_ARM_SERVO_2)
      self.arm_elevator_limit_switch = self.arm_elevator_motor.getReverseLimitSwitch(rev.SparkMaxLimitSwitch)
      self.arm_base_limit_switch = self.arm_base_motor.getReverseLimitSwitch(rev.SparkMaxLimitSwitch)

      # operator controller with buttons for features of robot
      self.operator_controller = wpilib.interfacs.GenericHID(constants.ID_CONTROLLER)
      
      # drive controller and rotary controller for driving and turning the robot
      self.drive_controller = wpilib.XboxController(constants.ID_CONTROLLER)
      self.rotary_controller = rotary_controller.RotaryJoystick(constants.ID_CONTROLLER)

      self.drive = drive.Drive(self.front_left, self.front_right, self.middle_left, self.middle_right, self.back_left, self.back_right)
      self.arm = arm.Arm(self.arm_elevator_motor, self.arm_base_motor, self.arm_end_servo_1, self.arm_end_servo_2, self.arm_elevator_limit_switch, self.arm_base_limit_switch, self.pid)
      self.balance = balance.Balance(self.drive_imu, self.drive, self.front_additional, self.back_additional)


      self.network_receiver = networking.NetworkReciever()

   def autonomoutInit(self):
      self.autonomous = autonomous.Autonomous(self.drive, self.arm, self.balance)

      self.AUTO_MODE_ONE = 0
      self.AUTO_MODE_TWO = 0
      self.AUTO_MODE = self.AUTO_MODE_ONE


   def autonomousPeriodic(self):
      # replace numbers with constants from constants.py file
      if self.AUTO_MODE == self.AUTO_MODE_ONE:
         self.autonomous.auto_mode_one()

      elif self.AUTO_MODE == self.AUTO_MODE_TWO:
         self.autonomous.auto_mode_two()

      else:
         # stop everything
         pass
      
   def teleopPeriodic(self):
      try:
         # check if each part of the robot is enabled or not before checking if buttons pressed, etc.
         if constants.ENABLE_DRIVING:
            joystick_y = math_functions.interpolation(self.drive_controller.getRawAxis(1))
            joystick_x = math_functions.interpolation(self.drive_controller.getRawAxis(0))
            angle = self.rotary_controller.rotary_inputs()

            self.drive.absolute_drive(joystick_y, joystick_x, angle, constants.DRIVE_MOTOR_POWER_MULTIPLIER)


         if constants.ENABLE_ARM:
            pass

         if constants.ENABLE_BALANCE:
            pass

      except:
         raise
         
if __name__ == "__main__":
   wpilib.run(MyRobot)
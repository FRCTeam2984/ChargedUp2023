import wpilib, rev, ctre
import math

from utils import math_functions, constants
from commands import networking, rotary_controller, drive

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

      # Drive class instance
      self.drive = drive.Drive(self.front_left, self.front_right, self.middle_left, self.middle_right, self.back_left, self.back_right)

      # Motors and servos that control arm
      self.arm_elevator_motor = rev.CANSparkMax(constants.ID_ARM_ELEVATOR)
      self.arm_chain_motor = rev.CANSparkMax(constants.ID_ARM_CHAIN)
      self.arm_end_servo = wpilib.Servo(constants.ID_ARM_SERVO)

      # operator controller with buttons for features of robot
      self.operator_controller = wpilib.interfacs.GenericHID(constants.ID_CONTROLLER)
      
      # drive controller and rotary controller for driving and turning the robot
      self.drive_controller = wpilib.XboxController(constants.ID_CONTROLLER)
      self.rotary_controller = rotary_controller.RotaryJoystick(constants.ID_CONTROLLER)

      self.network_receiver = networking.NetworkReciever()


   def autonomoutInit(self):
      self.timer.reset()
      self.timer.start()

      self.auto_stage = 0

   def autonomousPeriodic(self):
      # replace numbers with constants from constants.py file
      if self.AUTO_MODE == 0:
         if self.auto_stage == 0:
            pass
            self.auto_stage = 1
         
         if self.auto_stage == 1:
            pass
            self.auto_stage = 2

         if self.auto_stage == 2:
            pass
            self.auto_stage = 3

         if self.auto_stage == 4:
            pass
            self.auto_stage = 5

         if self.auto_stage == 5:
            pass
      
      elif self.AUTO_MODE == 1:
         if self.auto_stage == 0:
            pass
            self.auto_stage = 1
         
         if self.auto_stage == 1:
            pass
            self.auto_stage = 2

         if self.auto_stage == 2:
            pass
            self.auto_stage = 3

         if self.auto_stage == 4:
            pass
            self.auto_stage = 5

         if self.auto_stage == 5:
            pass


   def teleopPeriodic(self):
      try:
         # check if each part of the robot is enabled or not before checking if buttons pressed, etc.
         if constants.ENABLE_DRIVING:
            pass

         if constants.ENABLE_ARM:
            pass

         if constants.ENABLE_BALANCE:
            pass

      except:
         raise
         


if __name__ == "__main__":
   wpilib.run(MyRobot)
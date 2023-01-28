import wpilib, rev, ctre
import math

from utils import math_functions, constants
from commands import networking

class MyRobot(wpilib.TimedRobot): 

   def robotInit(self):
      self.timer = wpilib.Timer()

      # Front and back mecanum wheels are powered Falcon500 motors
      self.front_left = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_LEFT)
      self.front_right = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_RIGHT)
      self.back_left = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_LEFT)
      self.back_right = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_RIGHT)

      # Middle omni wheels are powered by Neo550 motors
      self.middle_right = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_RIGHT)
      self.middle_left = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_LEFT)

      # Motors and servos that control arm
      self.arm_elevator_motor = rev.CANSparkMax(constants.ID_ARM_ELEVATOR)
      self.arm_chain_motor = rev.CANSparkMax(constants.ID_ARM_CHAIN)
      self.arm_end_servo = wpilib.Servo(constants.ID_ARM_SERVO)

      self.joystick = wpilib.interfacs.GenericHID(constants.ID_CONTROLLER)

      self.AUTO_MODE = 0

      self.network_receiver = networking.NetworkReciever()


   def autonomoutInit(self):
      self.timer.reset()
      self.timer.start()

      self.auto_stage = 0

   def autonomousPeriodic(self):
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
         pass

      except:
         raise
         


if __name__ == "__main__":
   wpilib.run(MyRobot)
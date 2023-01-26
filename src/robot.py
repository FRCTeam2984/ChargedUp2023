import wpilib, rev, ctre
from utils import math_functions, constants
import math

class MyRobot(wpilib.TimedRobot): 

   def robotInit(self):
      self.timer = wpilib.Timer()

      # Front and back mecanum wheels are powered Falcon500 motors
      self.frontLeft = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_LEFT)
      self.frontRight = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_RIGHT)
      self.backLeft = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_LEFT)
      self.backRight = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_RIGHT)

      # Middle omni wheels are powered by Neo550 motors
      self.middleRight = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_RIGHT)
      self.middleLeft = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_LEFT)



   def autonomoutInit(self):
      self.timer.reset()
      self.timer.start()

   def autonomousPeriodic(self):
      pass

   def teleopPeriodic(self):
      pass

if __name__ == "__main__":
   wpilib.run(MyRobot)
import wpilib, rev, ctre

class MyRobot(wpilib.TimedRobot):

   def robotInit(self):
      self.timer = wpilib.Timer()

   def autonomoutInit(self):
      self.timer.reset()
      self.timer.start()

   def autonomousPeriodic(self):
      pass

   def teleopPeriodic(self):
      pass

if __name__ == "__main__":
   wpilib.run(MyRobot)
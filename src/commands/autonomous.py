from wpilib import Timer

from subsystems.drive import Drive
from subsystems.arm import Arm

from commands.balance import Balance

class Autonomous:
   def __init__(self, _drive : Drive, _arm : Arm, _balance : Balance):
      self.drive = _drive
      self.arm = _arm
      self.balance = _balance

      self.timer = Timer()

      # stages of autonomous can change later
      self.AUTO_IDLE = 0
      self.AUTO_PLACING_PIECE = 1
      self.AUTO_TURNING = 2
      self.AUTO_MOVING_OUT_COMMUNITY = 3
      self.AUTO_BALANCING = 4
      self.AUTO_RETRIEVING_PIECE = 5
      self.AUTO_DONE = 6
      self.auto_stage = self.AUTO_IDLE


   def get_timer(self):
      return self.timer.getFPGATimestamp()


   def auto_mode_one(self):
      if self.auto_stage == self.AUTO_IDLE:
            # check that we are good to start autonomous
            self.auto_stage = self.AUTO_PLACING_PIECE
         
      elif self.auto_stage == self.AUTO_PLACING_PIECE:
         self.auto_stage = self.AUTO_TURNING

      elif self.auto_stage == self.AUTO_TURNING:
         self.auto_stage = self.AUTO_MOVING_OUT_COMMUNITY

      elif self.auto_stage == self.AUTO_MOVING_OUT_COMMUNITY:
         self.drive.arcade_drive(0.2, 0)
         
         self.auto_stage = self.AUTO_BALANCING

      elif self.auto_stage == self.AUTO_BALANCING:
         self.balance.balance()
         self.auto_state = self.AUTO_RETRIEVING_PIECE

      elif self.auto_state == self.AUTO_RETRIEVING_PIECE:
         self.auto_state = self.AUTO_DONE

      elif self.auto_state == self.AUTO_DONE:
         pass

      else:
         self.state = self.AUTO_IDLE


   def auto_mode_two(self):
      pass
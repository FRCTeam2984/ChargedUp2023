from ctre import WPI_TalonSRX
from wpilib import DigitalInput, Timer

class Extension:
   def __init__(self, _arm_extension_motor : WPI_TalonSRX, _arm_extension_limit_switch : DigitalInput):
      self.arm_extension_motor = _arm_extension_motor
      self.arm_extension_limit_switch = _arm_extension_limit_switch

      self.timer = Timer()
      self.extension_start_time = 0.0

      self.RETRACTED = 0
      self.EXTENDING = 1
      self.FINISHED = 2
      self.state = self.FINISHED
      self.speed = 0.35

      # stop, extend, retract
      # motor set

   def set_speed(self, speed):      
      self.arm_extension_motor.set(speed)

   def stop(self):
      self.arm_extension_motor.set(0)

   def retracted(self):
      return not self.arm_extension_limit_switch.get()

   def extend_retract(self, extend_button, retract_button):      
      if self.state == self.RETRACTED:
         if extend_button:
            self.extension_start_time = self.timer.getFPGATimestamp()
            self.state = self.EXTENDING
            print("starting to extend")
         
         if retract_button and not self.retracted():
            self.set_speed(self.speed)
         else:
            self.stop()

      elif self.state == self.EXTENDING:
         if self.extension_start_time + 3 >= self.timer.getFPGATimestamp():
            self.set_speed(-self.speed)
            print("extending")

            if not extend_button:
               self.stop()

            if retract_button and not self.retracted():
               self.set_speed(self.speed)

            if self.retracted():
               self.state = self.RETRACTED
   

         else:
            self.state = self.FINISHED

      elif self.state == self.FINISHED:
         print("done extending")

         if self.retracted():
            self.state = self.RETRACTED

         if retract_button and not self.retracted():
            self.set_speed(self.speed)
         else:
            self.stop()

   """
   def retract(self):
      if not self.retracted():
         self.set_speed(0.2)
      else:
         self.stop()
         self.state = self.RETRACTED
   """
# pretty much just copied from last year with some changes

from wpilib import Joystick

class RotaryJoystick(Joystick):
   def __init__(self, id : int):
      # give methods and properties of parent (Joystick) class
      super().__init__(id)

      # initialize some variables
      self.angle_offset = 0.0
      self.setTwistChannel(4)


   def generate_angle_midmax(self, mid, _min, _max):
      midmax = ((mid - _min) / (_max - _min))
      return midmax


   def rotary_inputs(self):
      x = self.getX()
      y = self.getY()
      z = self.getZ()

      _max = max(x, y, z)
      _min = min(x, y, z)

      if (_max - _min) == 0:
         print("Joystick is not connected")

      else:
         if ((x <= y) and (y <= z)):
            # mid = y since it is greater that x but less than z
            mid = y

            angle = 60 - self.generate_angle_midmax(mid, _min, _max) * 60

         if ((y <= x) and (x <= z)):
            # mid = x since it is greater than y but less than z
            mid = x

            angle = 60 + self.generate_angle_midmax(mid, _min, _max) * 60

         if ((y <= z) and (z <= x)):
            # mid = z since it is greater than y but less than x
            mid = z

            angle = 180 - self.generate_angle_midmax(mid, _min, _max) * 60

         if ((z <= y) and (y <= x)):
            # mid = y since it is greater than z but less than x
            mid = y

            angle = 180 + self.generate_angle_midmax(mid, _min, _max) * 60

         if ((z <= x) and (x <= y)):
            # mid = x since it is greater than z but less than y
            mid = x

            angle = 300 - self.generate_angle_midmax(mid, _min, _max) * 60

         if ((x <= z) and (z <= y)):
            # mid = z since it is greater than x but less than y
            mid = z

            angle = 300 + self.generate_angle_midmax(mid, _min, _max) * 60

         angle += self.angle_offset

         return angle


   def reset_angle(self, angle):
      self.angle_offset = 0.0
      self.angle_offset = angle - self.rotary_inputs()
      #print(f"calling reset angle, offset = {self.angle_offset}")
   



   
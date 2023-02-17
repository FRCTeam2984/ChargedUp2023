from utils import constants


class Cube:
   def __init__(self):
      self.IDLE = 0
      self.TURNING = 1
      self.REACHING = 2
      self.DRIVING = 3
      self.GRABBING = 4
      self.RETRIEVING = 5
      self.state = self.IDLE

   def getCameraInfo(self):
      pass

   # turn towards the correct angle relative to the cube
   def turning(self):
      pass

   def arm_rotating(self, angle):
      pass

   def elevating(self, height):
      pass

   def driving(self):
      pass

   def grabbing(self):
      pass

   def retrieving(self):
      pass

   #need  x, y, limit_switch
   def place_cube(self, button_pressed, cube):
      if self.state == self.IDLE:
         # if button_pressed and cube is seen and arm is in default postion
         if button_pressed and cube:
            self.state = self.TURNING
      elif self.state == self.TURNING: 
         if button_pressed and cube:   
            if self.turning():
               self.state = self.REACHING
         else:
            self.state = self.IDLE
      elif self.state == self.REACHING:
         if button_pressed and cube:
            if self.arm_rotate(constants.CUBE_GROUND):
               if self.elevate(constants.ELEVATOR_LOW):
                  self.state = self.DRIVING
         else:
            self.state = self.IDLE
      elif self.state == self.DRIVING:
         if button_pressed and cube:
            if self.driving():
               self.state = self.GRABBING
         else:
            self.state = self.IDLE
      elif self.state == self.GRABBING:
         if button_pressed:
            if self.grabbing():
               self.state = self.RETRIEVING
         else:
            self.state = self.IDLE
      elif self.state == self.RETRIEVING:
         if button_pressed:
            if self.retrieving():
               pass
               #green LEDS flash yay
         else:
            self.state = self.IDLE
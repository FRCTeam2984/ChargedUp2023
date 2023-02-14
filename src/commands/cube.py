class Cube:
   IDLE = 0
   TURNING = 1
   REACHING = 2
   DRIVING = 3
   GRABBING = 4
   RETRIEVING = 5
   state = IDLE

   def place_cube(self, button_pressed, x, y, limit):
      if self.state == self.IDLE:
         if button_pressed:
            self.state = self.TURNING
      elif self.state == self.TURNING:
         pass
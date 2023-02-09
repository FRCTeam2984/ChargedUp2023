class PID:
   def __init__(self):
      self.p = 0
      self.i = 0
      self.d = 0
      
      self.previous_input = 0
      self.integral = 0

   def set_pid(self, p, i, d, val):
         self.p = p
         self.i = i
         self.d = d

         self.previous_input = val
         self.integral = 0

   def steer_pid(self, error):
         power = error * self.p

         if self.integral > 0 and (error * self.i < 0):
               self.integral = 0

         if (self.integral < 0) and (error * self.i > 0):
               self.integral = 0

         self.integral += error * self.i
         if (-20 < error) and (error < 20):
               power += self.integral
         
         else: 
               self.integral = 0

         power += (error - self.previous_input) * self.d
         self.previous_input = error
         
         return power
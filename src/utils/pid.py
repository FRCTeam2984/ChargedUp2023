class PID:
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
            self.integral += error*self.i
            if (-20 < error) and (error < 20):
                  power += self.integral
            else: 
                  self.integral=0
            power += (error - self.previous_input) * self.d
            self.previous_input = error
            return power
            

class NewPID:
   def __init__(self):
      self.Kp = 0
      self.Ki = 0
      self.Kd = 0

      self.previous_error = 0

      # integral term approximated using summation. Just adding up the error at very small time intervals kinda like a Riemann Sum
      self.integral_error = 0
      
      # change delta time to how often the drive function is called (how long it takes for one iteration of TeleopPeriodic)
      # guessing 1 second / 50 iterations per second = 0.02 seconds per iteration = 20ms
      self.delta_time = 0.02
   
   def evaluate(self, target_value, current_value):
      # target_value is the desired angle when turning the robot, and current_value is the current yaw of the robot from the IMU
      error =  target_value - current_value

      proportional_term = self.Kp * error
      
      # we need to estimate the derivative term using differentials
      difference = error - self.previous_error
      derivative = difference / self.delta_time
      derivative_term = self.Kd * derivative

      integral = error * self.delta_time
      integral_term = self.Ki * integral

      # add together the P, I, and D, values to get the adjustment we need to give to the motor
      adjustment = proportional_term + derivative_term + integral_term

      # set the previous error to the current error before the next iteration
      self.previous_error = error

      return adjustment





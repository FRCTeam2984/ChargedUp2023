from wpilib import Timer

from subsystems.arm import Arm
from subsystems.drive import Drive
from subsystems import networking
from utils import constants, imutil, math_functions

"""
1) raise the arm all the way
2) turn and drive so the cube is in the correct range on screen
3) open the cube arm and lower the cone arm
4) lower the arm completely
5) close the cube arm
6) raise the arm a bit
"""

class Cube:
   def __init__(self, _arm : Arm, _drive : Drive, _drive_imu : imutil.Imutil, _network_reciever : networking.NetworkReciever, _timer : Timer):
      self.IDLE = 0
      self.RAISING_ARM = 1
      self.DRIVING = 2
      self.LOWERING = 4
      self.WAITING = 5
      self.GRABBING = 6
      self.RAISING = 7
      self.state = self.IDLE

      self.timer = _timer
      self.start_time = 0.0

      self.desired_angle = 0.0
      self.previous_image_count = -1

      self.networking = _network_reciever
      self.drive_imu = _drive_imu

      self.arm = _arm
      self.drive = _drive

   def raising_arm(self):
      self.arm.base_desired_position = 5

      self.arm.lower_cone_arm()
      self.arm.open_cube_arm()

      if self.arm.base_close_enough():
         return True

   def driving(self):
      cube_data = self.networking.find_cube()

      x = cube_data[1]
      y = cube_data[2] + 195
      counter = cube_data[3]

      if self.previous_image_count != counter:
         angle_change = (x + 70) * 0.15
         self.desired_angle = angle_change + self.drive_imu.get_yaw()
         self.previous_image_count = counter
         #print(f"cube data = {cube_data}")

      forward_speed = 0
      if y < -50:
         forward_speed = 1.5
      elif y < -30:
         forward_speed = 0.6
      elif y > -30 and y < -2:
         forward_speed = 0.5
      elif y > 50:
         forward_speed = -1.5
      elif y > 30:
         forward_speed = -0.6
      elif y < 30 and y > 2:
         forward_speed = -0.5
      
      
      #forward_speed = (y + 200) * 0.005 * -1

      #print(f"angle_change = {self.desired_angle}, forward_speed = {forward_speed}")

      if cube_data[0]:
         self.drive.absolute_drive(forward_speed, 0, self.desired_angle, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)
         constants.CONTROL_OVERRIDE = True

      print(f"x = {x}, y = {y}")
      if math_functions.in_range(x, -80, -65) and math_functions.in_range(y, -3, 3):
         return True


   def lowering(self):
      self.arm.base_desired_position = 27

      if self.arm.base_close_enough():
         return True

   def waiting(self):
      if self.start_time + 0.75 < self.timer.getFPGATimestamp():
         return True

   def grabbing(self):
      self.arm.close_cube_arm()

      if self.start_time + 0.5 < self.timer.getFPGATimestamp():
         return True

   def raising_final(self):
      self.arm.base_desired_position = 15

      if self.arm.base_close_enough():
         return True


   #need  x, y, limit_switch
   def pickup_cube(self, button_is_pressed, cube_is_seen):
      if button_is_pressed:

         if self.state == self.IDLE:
            self.arm.base_desired_position = 3

         if cube_is_seen:
            # idle, reaching, grabbing, retreiving, stop
            # arm_rotating, grabbing, retreiving
            if self.state == self.IDLE:
               # if button_pressed and cube is seen and arm is in default postion
               #self.state = self.TURNING
               self.state = self.RAISING_ARM
               print("raising arm")


            elif self.state == self.RAISING_ARM: 
               if self.raising_arm():
                  self.state = self.DRIVING
                  print("driving")


            elif self.state == self.DRIVING:
               if self.driving():
                 self.state = self.LOWERING
                 print("lowering")
                 self.start_time = self.timer.getFPGATimestamp()

            elif self.state == self.LOWERING:
               if self.lowering():
                  self.state = self.WAITING
                  print("waiting")
                  self.start_time = self.timer.getFPGATimestamp()

            elif self.state == self.WAITING:
               print(f"start time = {self.start_time}, current time = {self.timer.getFPGATimestamp()}, arm = {self.arm.base_desired_position}")

               if self.waiting():
                  self.state = self.GRABBING
                  print("grabbing")
                  self.start_time = self.timer.getFPGATimestamp()

            elif self.state == self.GRABBING:
               if self.grabbing():
                  self.state = self.RAISING
                  print("raising")
                  self.start_time = self.timer.getFPGATimestamp()

            elif self.state == self.RAISING:
               if self.raising_final():
                  print("done!")
                  #green LEDS flash yay

         else: self.state = self.IDLE
      else: self.state = self.IDLE
      #self.drive.stop_drive()
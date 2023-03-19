from wpilib import Timer

from subsystems.arm import Arm
from subsystems.drive import Drive
from subsystems import networking
from utils import constants, imutil

class Cube:
   def __init__(self, _arm : Arm, _drivetrain : Drive, _drive_imu : imutil.Imutil, _timer : Timer):
      self.IDLE = 0
      self.TURNING = 1
      self.REACHING = 2
      self.DRIVING = 3
      self.GRABBING = 4
      self.RAISING = 5
      self.RETRIEVING = 6
      self.state = self.IDLE

      self.timer = _timer

      #self.networking = networking.NetworkReciever()
      self.drive_imu = _drive_imu

      self.arm = _arm
      self.drivetrain = _drivetrain


   def get_camera_info(self):
      #x = self.networking.find_cube()[1]
      #y = self.networking.find_cube()[2]

      x = 0
      y = 0
      
      return [x, y]

   # turn towards the correct angle relative to the cube
   def turning(self):
      #self.drivetrain.absolute_drive(0, 0, self.drive_imu + self.get_camera_info()[0] + constants.CUBE_OFFSET, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)
      #if abs(self.get_camera_info()[0]) < 5:
      #   return True
      pass
      
   def arm_rotate(self):
      self.arm.position_ground()
      if self.arm.position == self.arm.GROUND:
         return True
      else:
         return False

   def driving(self):
      #self.drivetrain.absolute_drive(.1, 0, self.drive_imu + self.get_camera_info()[0] + constants.CUBE_OFFSET, 1)
      #if self.get_camera_info()[1] < constants.CUBE_COLLECT_Y:
      #   return
      pass


   def grabbing(self):
      self.arm.lower_cone_arm()

      print(f"timer value = {self.timer.getFPGATimestamp()}, start time = {self.start_time}")

      if self.start_time + 1 < self.timer.getFPGATimestamp():
         self.arm.close_cube_arm()
         return True

      #if self.arm.cube_arm_closed_enough():
      #   return True
      
      # add later wait a certain amount of time to close


   def raising(self):
      """
      if self.arm.position_elevator_top():
         return True
      else:
         return False
      """
      return True


   def retrieving(self):
      self.arm.position_home()
      if self.arm.position == self.arm.HOME:
         return True


   #need  x, y, limit_switch
   def pickup_cube(self, button_is_pressed, cube_is_seen):
      if button_is_pressed:
         if cube_is_seen:
            # idle, reaching, grabbing, retreiving, stop
            # arm_rotating, grabbing, retreiving
            if self.state == self.IDLE:
               # if button_pressed and cube is seen and arm is in default postion
               #self.state = self.TURNING
               self.state = self.REACHING
               print("moving to reaching state")



            elif self.state == self.TURNING: 
               if self.turning():
                  self.state = self.REACHING



            elif self.state == self.REACHING:
               if self.arm_rotate():
                 # self.state = self.DRIVING
                 self.state = self.GRABBING
                 self.start_time = self.timer.getFPGATimestamp()
                 print("done reaching")
  


            elif self.state == self.DRIVING:
               if self.driving():
                  self.state = self.GRABBING
                  self.start_time = self.timer.getFPGATimestamp()



            elif self.state == self.GRABBING:
               if self.grabbing():
                  self.state = self.RAISING
                  print("done grabbing")


            elif self.state == self.RAISING:
               if self.raising():
                  self.state = self.RETRIEVING
                  print("done raising")
               


            elif self.state == self.RETRIEVING:
               if self.retrieving():
                  pass
                  print("done retrieving")
                  #green LEDS flash yay


         else: self.state = self.IDLE
      else: self.state = self.IDLE
      self.drivetrain.stop_drive()
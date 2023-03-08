from subsystems.arm import Arm
from subsystems.drive import Drive
from subsystems import networking
from utils import constants, imutil


class Cube:
   def __init__(self, _arm : Arm, _drivetrain : Drive, _drive_imu : imutil.Imutil):
      self.IDLE = 0
      self.TURNING = 1
      self.REACHING = 2
      self.DRIVING = 3
      self.GRABBING = 4
      self.RETRIEVING = 5
      self.state = self.IDLE

      self.networking = networking.NetworkReciever()
      self.drive_imu = _drive_imu

      self.arm = _arm
      self.drivetrain = _drivetrain


   def get_camera_info(self):
      x = self.networking.find_cube()[1]
      y = self.networking.find_cube()[2]
      return [x, y]

   # turn towards the correct angle relative to the cube
   def turning(self):
      Drive.absolute_drive(0, 0, self.drive_imu + self.get_camera_info()[0] + constants.CUBE_OFFSET, 1)
      if abs(self.get_camera_info()[0]) < 5:
         return True
      
   def arm_rotating(self):
      self.arm.position_ground()
      if self.arm.position == self.arm.GROUND:
         return True


   def elevating(self, height):
      self.arm.position_ground()
      if self.arm.position == self.arm.GROUND:
         return True

   def driving(self):
      Drive.absolute_drive(.1, 0, self.drive_imu + self.get_camera_info()[0] + constants.CUBE_OFFSET, 1)
      if self.get_camera_info()[1] < constants.CUBE_COLLECT_Y:
         return

   def grabbing(self, limit):
      Arm.set_servo_cube_angle(constants.CUBE_SERVO_ANGLE)
      if limit:
         return True

   def retrieving(self):
      self.arm.position_home()
      if self.arm.position == self.arm.HOME:
         return True

   #need  x, y, limit_switch
   def pickup_cube(self, button_is_pressed, cube_is_seen, limit):
      if button_is_pressed:
         if cube_is_seen:
            if self.state == self.IDLE:
               # if button_pressed and cube is seen and arm is in default postion
               self.state = self.TURNING

            elif self.state == self.TURNING: 
               if self.turning():
                  self.state = self.REACHING
               else:
                  self.state = self.IDLE

            elif self.state == self.REACHING:
               if self.arm_rotate():
                  if self.elevate():
                     self.state = self.DRIVING
               else:
                  self.state = self.IDLE

            elif self.state == self.DRIVING:
               if self.driving():
                  self.state = self.GRABBING
               else:
                  self.state = self.IDLE

            elif self.state == self.GRABBING:
               if self.grabbing(limit):
                  self.state = self.RETRIEVING
               else:
                  self.state = self.IDLE
               
            elif self.state == self.RETRIEVING:
               if self.retrieving():
                  pass
                  #green LEDS flash yay
               else:
                  self.state = self.IDLE
         else: self.state = self.IDLE
      else: self.state = self.IDLE
      Drive.stop_drive()
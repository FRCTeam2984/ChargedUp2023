from subsystems.arm import Arm
from subsystems.drive import Drive

from utils import constants


class Cone:
   def __init__(self, _arm : Arm, _drivetrain : Drive):
      self.arm = _arm
      self.drivetrain = _drivetrain

      # steps are not necessarily in order, just the different things we need to do
      self.IDLE = 0
      self.LOWERING_ARM = 1
      self.DRIVING_FORWARD = 2
      self.GRABBING_CONE = 3
      self.MOVING_ARM_IN = 4
      self.ROTATING_ARM = 5
      self.ROTATING_ARM_SECOND = 6
      self.FINISHED = 7
      self.state = self.IDLE

      # idk how we want to handle cones but this is simple
      # simplify the constants file by putting cone positions in this file later
      self.located_cone = constants.NO_CONE
      

   def locate_cone(self):
      pass

   # the following functions until pickup_cone() return a boolean value if the corresponding action has been completed

   def able_to_start(self):
      return True

   def bottom_limit_switch_pressed(self):
      return self.arm.arm_bottom_limit_switch.get()
   

   def robot_close_enough(self):
      # needs camera code to work properly
      return True
   
   def has_grabbed_cone(self):
      # idk how to do this check later
      return True
   
   def arm_is_home(self):
      # arm code .position() to return the current position and check if it is in the home position
      if self.arm.position == self.arm.HOME:
         return True
      
      else:
         return False

   def arm_rotated_enough(self):
      # figure out how to do this probably just getting servo position
      return True
   
   def arm_rotated_enough_second(self):
      # same as above probably just get servo position
      return True

   def pickup_cone(self, button_is_pressed, cube_is_seen):
      if self.located_cone == constants.CONE_FACING_TOWARDS:
         # state machine is the cone is knocked over and the base is facing towards the robot
         if self.state == self.IDLE:
            if (self.able_to_start()):
               self.state = self.LOWERING_ARM

            else:
               return

         elif self.state == self.LOWERING_ARM:
            self.arm.position_ground()

            if (self.bottom_limit_switch_pressed()):
               self.state = self.DRIVING_FORWARD

         elif self.state == self.DRIVING_FORWARD:
            # how do we determine how many iterations or how much to drive forward?
            self.drivetrain.set_speed(2)

            # check in some way if the robot is close enough to the cone
            if (self.robot_close_enough()):
               self.state = self.GRABBING_CONE

         elif self.state == self.GRABBING_CONE:
            # do something to grab the cone, might not be necessary later

            if (self.has_grabbed_cone()):
               self.state = self.MOVING_ARM_IN

         elif self.state == self.MOVING_ARM_IN:
            self.arm.position_home()

            # check if the arm has been moved back into the robot
            if (self.arm_is_home()):
               self.state = self.FINISHED
               return 0

      if self.located_cone == constants.CONE_FACING_AWAY:
         if self.state == self.IDLE:
            # check to make sure nothing is conflicting
            self.state = self.LOWERING_ARM

         elif self.state == self.LOWERING_ARM:
            self.arm.position_ground()

            # check to make sure a bottom limit switch on the arm is pressed or something before moving on
            if (self.bottom_limit_switch_pressed()):
               self.state = None

         elif self.state == self.ROTATING_ARM:
            # rotate the arm to the left or right figure out logic to do this later
            # ~ 20 degrees
            pass

            if (self.arm_rotated_enough()):
               self.state = self.DRIVING_FORWARD

         elif self.state == self.DRIVING_FORWARD:
            self.drivetrain.set_speed(2)

            if (self.robot_close_enough()):
               self.state = self.ROTATING_ARM_SECOND

         elif self.state == self.ROTATING_ARM_SECOND:
            # rotate arm in the opposite direction is was rotated in earlier ~ 20 degrees
            pass

            # need to check which case this results in, but i'll just say it is "finished" for now
            if (self.arm_rotated_enough_second()):
               self.state = self.FINISHED
               return 0

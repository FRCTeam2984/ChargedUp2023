import wpilib, rev, ctre
import math
from subsystems import arm, drive, networking, rotary_controller

from utils import math_functions, constants, imutil, pid
from commands import balance, cone, cube, autonomous

"""
NOTE:
BRING EXTRA VRM CABLES TO COMPETITION IN CASE OF SATEFY INSPECTION IDK ASK GREG

TO DO FOR ANY MEETING:
- modes of autonomous
- figure out how to find position of arm without limit switch encoder complicated situation
- polish the PID code (mainly the new stuff i wrote to understand it better)
- state machine format for arm positions
- generally, commands for balancing and moving arms, etc.
"""

class MyRobot(wpilib.TimedRobot): 
   def robotInit(self):
      self.timer = wpilib.Timer()

      # Front and back mecanum wheels are powered Falcon500 motors and drive class instance
      self.front_left = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_LEFT)
      self.front_right = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_RIGHT)
      self.back_left = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_LEFT)
      self.back_right = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_RIGHT)

      # Middle omni wheels are powered by Neo550 motors
      self.middle_right = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_RIGHT, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
      self.middle_left = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_LEFT, rev.CANSparkMaxLowLevel.MotorType.kBrushless)

      self.front_additional = ctre.WPI_TalonSRX(constants.ID_ADDITIONAL_FRONT)
      self.back_additional = ctre.WPI_TalonSRX(constants.ID_ADDITIONAL_BACK)

      # imu and pid stuff to be added below
      # using the middle left motor, even though the middle right one can be used too
      self.imu_talon = ctre.WPI_TalonSRX(constants.ID_IMU_TALON)
      self.drive_imu = imutil.Imutil(self.imu_talon)

      self.pid = pid.PID()
      self.elevator_pid = pid.PID()
      self.base_pid = pid.PID()

      # Motors and servos that control arm
      self.arm_elevator_motor = rev.CANSparkMax(constants.ID_ARM_ELEVATOR, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
      self.arm_base_motor = rev.CANSparkMax(constants.ID_ARM_BASE, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
      self.arm_end_servo_cube = wpilib.Servo(constants.ID_ARM_SERVO_CUBE)
      self.arm_end_servo_cone = wpilib.Servo(constants.ID_ARM_SERVO_CONE)
      self.arm_cube_limit_switch = wpilib.DigitalInput(constants.ID_ARM_CUBE_LIMIT_SWITCH)

      self.drive = drive.Drive(self.front_left, self.front_right, self.middle_left, self.middle_right, self.back_left, self.back_right, self.drive_imu, self.pid)
      self.arm = arm.Arm(self.arm_elevator_motor, self.arm_base_motor, self.arm_end_servo_cube, self.arm_end_servo_cone, self.arm_cube_limit_switch, self.elevator_pid, self.base_pid)
      self.balance = balance.Balance(self.drive_imu, self.drive, self.front_additional, self.back_additional)

      self.network_receiver = networking.NetworkReciever()

   def autonomoutInit(self):
      self.autonomous = autonomous.Autonomous(self.drive, self.arm, self.balance)

      self.AUTO_MODE_ONE = 0
      self.AUTO_MODE_TWO = 0
      self.AUTO_MODE = self.AUTO_MODE_ONE


   def autonomousPeriodic(self):
      # replace numbers with constants from constants.py file
      if self.AUTO_MODE == self.AUTO_MODE_ONE:
         self.autonomous.auto_mode_one()

      elif self.AUTO_MODE == self.AUTO_MODE_TWO:
         self.autonomous.auto_mode_two()

      else:
         # stop everything
         pass

   def teleopInit(self):
      while not wpilib.Joystick(constants.ID_ROTARY_CONTROLLER).getRawButton(12) or wpilib.Joystick(constants.ID_OPERATOR_CONTROLLER).getRawButton(12):
         # switch operator and rotary ids
         temp = constants.ID_OPERATOR_CONTROLLER
         constants.ID_OPERATOR_CONTROLLER = constants.ID_ROTARY_CONTROLLER
         constants.ID_ROTARY_CONTROLLER = temp

         print(f"operator = {constants.ID_OPERATOR_CONTROLLER}, rotary = {constants.ID_ROTARY_CONTROLLER}")


      self.rotary_controller = rotary_controller.RotaryJoystick(constants.ID_ROTARY_CONTROLLER)
      self.rotary_buttons = wpilib.interfaces.GenericHID(constants.ID_ROTARY_CONTROLLER)

      self.operator_controller = wpilib.interfaces.GenericHID(constants.ID_OPERATOR_CONTROLLER)
      self.drive_joystick = wpilib.XboxController(constants.ID_DRIVE_CONTROLLER)

      self.arm.elevator_desired_position = 10
      self.arm.base_desired_position = 10

   def teleopPeriodic(self):
      try:
         if (self.arm.elevator_encoder_zero == 0.12345):
            self.arm.calibrate_elevator()

         else:
            self.arm.set_elevator_position(self.arm.elevator_desired_position)
            #print(f"elev encoder = {self.arm.elevator_encoder_zero}")
   

         """
         if (self.arm.base_encoder_zero == 0.12345):
            self.arm.calibrate_base()

         else:
            self.arm.set_base_position(self.arm.base_desired_position)

         """

         print(f"elevator (z, p, d) = {self.arm.elevator_encoder_zero}, {self.arm.get_elevator_motor_encoder() - self.arm.elevator_encoder_zero}, {self.arm.elevator_desired_position} \
              base (z, p, d) = {self.arm.base_encoder_zero}, {self.arm.get_base_motor_encoder() - self.arm.base_encoder_zero}, {self.arm.base_desired_position}")

         # check if each part of the robot is enabled or not before checking if buttons pressed, etc.         
         if constants.ENABLE_DRIVING:
            joystick_y = math_functions.interpolation(self.drive_joystick.getRawAxis(1))
            joystick_x = math_functions.interpolation(self.drive_joystick.getRawAxis(0))
            angle = self.rotary_controller.rotary_inputs()

            print(f"speed (y): {joystick_y}, left_right (x): {joystick_x}")

            self.drive.absolute_drive(joystick_y, joystick_x, angle, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)

         if constants.ENABLE_ARM:
            raise_elevator = self.operator_controller.getRawButton(1)
            lower_elevator = self.operator_controller.getRawButton(2)

            lift_arm = self.operator_controller.getRawButton(3)
            lower_arm = self.operator_controller.getRawButton(4)

            open_cube_arm = self.operator_controller.getRawButton(5)
            close_cube_arm = self.operator_controller.getRawButton(6)

            lower_cone_arm = self.operator_controller.getRawButton(9)
            raise_cone_arm = self.operator_controller.getRawButton(10)


            if self.operator_controller.getRawButton(11):
               self.arm.elevator_desired_position = 100

            if self.operator_controller.getRawButton(12):
               self.arm.base_desired_position = 100

            if self.rotary_buttons.getRawButton(1):
               self.arm.elevator_desired_position = 10
               self.arm.base_desired_position = 10


            if raise_elevator:
               #print("raise elevator")
               self.arm.set_elevator_speed(0.3)

            elif lower_elevator:
               #print("lower elevator")
               self.arm.set_elevator_speed(-0.3)

            else:
               self.arm.stop_elevator()
            

            if lift_arm:
               self.arm.set_base_speed(0.17)

            elif lower_arm:
               self.arm.set_base_speed(-0.17)

            else:
               self.arm.stop_base()




            if open_cube_arm:
               print("opening cube arm")
               self.arm.open_cube_arm()

            elif close_cube_arm:
               print("closing cube arm")
               self.arm.close_cube_arm()


            
            if raise_cone_arm:
               print("raising cone arm")
               self.arm.lift_cone_arm()

            elif lower_cone_arm:
               print("lowering cone arm")
               self.arm.lower_cone_arm()


         if constants.ENABLE_BALANCE:
            pass

      except:
         raise
         
if __name__ == "__main__":
   wpilib.run(MyRobot)
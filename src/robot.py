import wpilib, rev, ctre
import math
from subsystems import arm, drive, networking, rotary_controller, camera_led

from utils import math_functions, constants, imutil, pid
from commands import balance, cone, cube, autonomous

"""
NOTE:
BRING EXTRA VRM CABLES TO COMPETITION IN CASE OF SATEFY INSPECTION IDK ASK GREG

TO DO 3/19 MEETING:
- 3 modes of autonomous test a lot left and right especially
- start auto picking up and state machines including driving and camera stuff
"""

class MyRobot(wpilib.TimedRobot): 
   def robotInit(self):
      self.timer = wpilib.Timer()
      self.last_printout = 0.0

      # Front and back mecanum wheels are powered Falcon500 motors and drive class instance
      self.front_left = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_LEFT)
      self.front_right = ctre.WPI_TalonFX(constants.ID_DRIVE_FRONT_RIGHT)
      self.back_left = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_LEFT)
      self.back_right = ctre.WPI_TalonFX(constants.ID_DRIVE_BACK_RIGHT)

      # Middle omni wheels are powered by Neo550 motors
      self.middle_right = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_RIGHT, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
      self.middle_left = rev.CANSparkMax(constants.ID_DRIVE_MIDDLE_LEFT, rev.CANSparkMaxLowLevel.MotorType.kBrushless)

      # imu and pid stuff to be added below
      # using the middle left motor, even though the middle right one can be used too
      self.imu_talon = ctre.WPI_TalonSRX(constants.ID_IMU_TALON)
      self.drive_imu = imutil.Imutil(self.imu_talon)
      self.drive_imu_init = self.drive_imu.get_yaw()

      self.pid = pid.PID()
      #self.elevator_pid = pid.PID()
      self.base_pid = pid.PID()

      # Motors and servos that control arm
      #self.arm_elevator_motor = rev.CANSparkMax(constants.ID_ARM_ELEVATOR, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
      self.arm_base_motor = rev.CANSparkMax(constants.ID_ARM_BASE, rev.CANSparkMaxLowLevel.MotorType.kBrushless)
      self.arm_end_servo_cube = wpilib.Servo(constants.ID_ARM_SERVO_CUBE)
      self.arm_end_servo_cone = wpilib.Servo(constants.ID_ARM_SERVO_CONE)
      self.arm_cube_limit_switch = wpilib.DigitalInput(constants.ID_ARM_CUBE_LIMIT_SWITCH)

      self.drive = drive.Drive(self.front_left, self.front_right, self.middle_left, self.middle_right, self.back_left, self.back_right, self.drive_imu, self.pid)
      
      self.arm = arm.Arm(self.arm_base_motor, self.arm_end_servo_cube, self.arm_end_servo_cone, self.arm_cube_limit_switch, self.base_pid)
      self.arm_desired_temp = 0
      
      self.balance = balance.Balance(self.drive, self.drive_imu)

      self.camera_left_led = wpilib.PWM(2)
      self.camera_right_led = None
      self.camera_led = camera_led.Camera_LED(self.camera_left_led, self.camera_right_led)

      self.network_receiver = networking.NetworkReciever()
      self.network_receiver.dashboard.putBoolean("run_cube", True)
      self.network_receiver.dashboard.putBoolean("run_cone", True)
      self.network_receiver.dashboard.putBoolean("run_apriltag", True)

      self.auto_cube = cube.Cube(self.arm, self.drive, self.drive_imu, self.network_receiver, self.timer)

      self.autonomous_switch_left = wpilib.DigitalInput(2)
      self.autonmous_switch_right = wpilib.DigitalInput(1)
      # both high = straight
      # right high left low go left
      # left high right low go right

      self.rotary_controller = rotary_controller.RotaryJoystick(constants.ID_ROTARY_CONTROLLER)
      self.rotary_buttons = wpilib.interfaces.GenericHID(constants.ID_ROTARY_CONTROLLER)

      self.operator_controller = wpilib.interfaces.GenericHID(constants.ID_OPERATOR_CONTROLLER)
      self.drive_joystick = wpilib.XboxController(constants.ID_DRIVE_CONTROLLER)


   def autonomousInit(self):
      self.autonomous = autonomous.Autonomous(self.drive, self.arm, self.balance, self.autonomous_switch_left, self.autonmous_switch_right)

      self.AUTO_MODE_ONE = 0
      self.AUTO_MODE = self.AUTO_MODE_ONE

      self.drive_imu_init = self.drive_imu.get_yaw()

      self.rotary_controller.reset_angle(self.drive_imu.get_yaw())
      
   def autonomousPeriodic(self):
      constants.CONTROL_OVERRIDE = False

      self.imu_talon.set(0)
      self.autonomous.autonomous(self.drive_imu_init)

      """if type(self.drive_imu_init) != float:
         self.drive_imu_init = self.drive_imu.get_yaw()
         print(f"imu yaw = {self.drive_imu_init}")
         self.rotary_controller.reset_angle(self.drive_imu_init)"""

   def teleopInit(self):
      while not wpilib.Joystick(constants.ID_ROTARY_CONTROLLER).getRawButton(12) or wpilib.Joystick(constants.ID_OPERATOR_CONTROLLER).getRawButton(12):
         # switch operator and rotary ids
         temp = constants.ID_OPERATOR_CONTROLLER
         constants.ID_OPERATOR_CONTROLLER = constants.ID_ROTARY_CONTROLLER
         constants.ID_ROTARY_CONTROLLER = temp

         print(f"operator = {constants.ID_OPERATOR_CONTROLLER}, rotary = {constants.ID_ROTARY_CONTROLLER}")


      self.arm.base_encoder_zero = 0.12345

      # maybe we need to reset the rotary controller angle in other places too
      self.arm.open_cube_arm()
      #self.arm.lift_cone_arm()

      self.rotary_controller.reset_angle(self.drive_imu.get_yaw())

      self.arm.base_desired_position = 10

      self.last_printout = self.timer.getFPGATimestamp()

   def teleopPeriodic(self):
      constants.CONTROL_OVERRIDE = False

      if self.last_printout + 1 < self.timer.getFPGATimestamp():
         #print(f"cube data = {self.network_receiver.find_cube()}")
         self.last_printout = self.timer.getFPGATimestamp()

      try:
         #self.camera_led.set_left_led(100)

         """if (self.arm.elevator_encoder_zero == 0.12345):
            self.arm.calibrate_elevator()

         else:
            self.arm.set_elevator_position(self.arm.elevator_desired_position)

            if (self.arm.base_encoder_zero == 0.12345):
               self.arm.calibrate_base()

            else:
               self.arm.set_base_position(self.arm.base_desired_position)"""

         if (self.arm.base_encoder_zero == 0.12345):
            self.arm.calibrate_base()

         else:
            self.arm.set_base_position(self.arm.base_desired_position)

         #print(f"elevator (z, p, d) = {self.arm.elevator_encoder_zero}, {self.arm.elevator_encoder_zero - self.arm.get_elevator_motor_encoder()}, {self.arm.elevator_desired_position}")
         #print(f"base (z, p, d) = {self.arm.base_encoder_zero}, {self.arm.base_encoder_zero - self.arm.get_base_motor_encoder()}, {self.arm.base_desired_position}")

         if constants.ENABLE_ARM:
            arm_controller_position = self.drive_joystick.getRawAxis(2)
            #print(f"arm_controller_position = {arm_controller_position}")

            self.arm_desired_temp = self.arm.base_encoder_in * arm_controller_position
            #print(f"arm desired position = {self.arm.base_desired_position}")

            # get ready to pick up cube
            if self.operator_controller.getRawButton(1):
               self.arm.open_cube_arm()
               self.arm.lift_cone_arm()

            if self.operator_controller.getRawButton(2):
               self.arm.lower_cone_arm()

            # close cube arm
            if self.operator_controller.getRawButton(3):
               self.arm.close_cube_arm()

            if self.operator_controller.getRawButton(10):
               self.arm_desired_temp = 10.5


            if self.operator_controller.getRawButton(6):
               self.network_receiver.dashboard.putBoolean("run_cube", False)
               self.network_receiver.dashboard.putBoolean("run_cone", False)
               self.network_receiver.dashboard.putBoolean("run_apriltag", False)

               constants.ARM_OVERRIDE = True

               cube_data = self.network_receiver.find_cube()
               cube_is_seen = False

               if cube_data != None:
                  cube_is_seen = cube_data[0]

               self.auto_cube.pickup_cube(True, cube_is_seen)
            
            else:
               self.auto_cube.state = self.auto_cube.IDLE

            """if self.operator_controller.getRawButton(1):
               self.arm.set_base_speed(0.2)

            elif self.operator_controller.getRawButton(2):
               self.arm.set_base_speed(-0.2)

            else:
               self.arm.stop_base()"""

         """if self.operator_controller.getRawButton(4):
               self.auto_cube.pickup_cube(True, True)
            
            # cube ground position
            if self.operator_controller.getRawButton(11):
               #self.arm.elevator_desired_position = 40
               self.arm.base_desired_position = 7

            # cube one position
            if self.operator_controller.getRawButton(12):
               #self.arm.elevator_desired_position = 40
               self.arm.base_desired_position = 27

            # cube two position
            if self.rotary_buttons.getRawButton(1):
               #self.arm.elevator_desired_position = 40
               self.arm.base_desired_position = 30

             # cone one starting position (first)
            if self.rotary_buttons.getRawButton(3):
               #self.arm.elevator_desired_position = 5
               self.arm.base_desired_position = 30

            # cone one lowered elevator position (second)
            if self.rotary_buttons.getRawButton(2):
               #self.arm.elevator_desired_position = 125
               pass

            # cone one lowered arm position (third)
            if self.rotary_buttons.getRawButton(4):
               self.arm.base_desired_position = 15


            # cone two starting position (first)
            if self.operator_controller.getRawButton(1):
               #self.arm.elevator_desired_position = 5
               self.arm.base_desired_position = 30

            # cone two lowered elevator position (second)
            if self.operator_controller.getRawButton(2):
               #self.arm.elevator_desired_position = 125
               pass

            # cone two lowered arm position (third)
            if self.operator_controller.getRawButton(3):
               self.arm.base_desired_position = 25
               self.arm.lower_cone_arm() 


            # elevator top height
            if self.operator_controller.getRawButton(5):
               #self.arm.elevator_desired_position = 5
               pass

            if self.operator_controller.getRawButton(6):
               #self.arm.elevator_desired_position = 100
               pass


            if self.operator_controller.getRawButton(9):
               self.balance.auto_balance()"""


         
         # check if each part of the robot is enabled or not before checking if buttons pressed, etc.         
         if constants.ENABLE_DRIVING:
            joystick_y = math_functions.interpolation(self.drive_joystick.getRawAxis(1))
            joystick_x = math_functions.interpolation(self.drive_joystick.getRawAxis(0))
            angle = self.rotary_controller.rotary_inputs()

            #print(f"speed (y): {joystick_y}, left_right (x): {joystick_x}, angle: {angle}, arm_controller = {self.drive_joystick.getRawAxis(2)}")

            #print(f"imu test = {self.drive_imu.test}")

            """if type(self.drive_imu_init) != float:
               self.drive_imu_init = self.drive_imu.get_yaw()
               #print(f"teleop imu angle = {self.drive_imu_init}")
               self.rotary_controller.reset_angle(self.drive_imu_init)"""

            if constants.CONTROL_OVERRIDE:
               self.rotary_controller.reset_angle(self.drive_imu.get_yaw())
               #print(f"yaw = {self.drive_imu.get_yaw()}, rotary input = {self.rotary_controller.rotary_inputs()}, rotary offset = {self.rotary_controller.angle_offset}")
            else:
               self.drive.absolute_drive(joystick_y, joystick_x, angle, True, constants.DRIVE_MOTOR_POWER_MULTIPLIER)
               #print("joystick control")


         if constants.ENABLE_BALANCE:
            pass

         if not constants.ARM_OVERRIDE:
            self.arm.base_desired_position = self.arm_desired_temp
               

         #self.network_receiver.test()

      except:
         raise
         
if __name__ == "__main__":
   wpilib.run(MyRobot)
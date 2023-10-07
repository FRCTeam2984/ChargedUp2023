"""
Orientation of the motors is as if you were standing at the back of the robot and looking towards it
"""

CONTROL_OVERRIDE = True
ARM_OVERRIDE = True

# Enable/disable feature
# make sure to change whenever testing
ENABLE_DRIVING = True
ENABLE_ARM = True
ENABLE_BALANCE = False

# positions that a cone can be in
NO_CONE = 0
CONE_FACING_TOWARDS = 1
CONE_FACING_AWAY = 2
CONE_STANDING_UP = 3

#positions the arm can be in for the cube (change when testing)
CUBE_GROUND = 123
CUBE_MID_HEIGHT = 456
CUBE_TALL_HEIGHT = 789

#positions the elevator can be in
ELEVATOR_LOW = 0
ELEVATOR_HIGH = 999

CUBE_OFFSET = 5

CUBE_COLLECT_Y =168738

CUBE_SERVO_ANGLE = 97287

# drive multipliers/power regulations
# might need to change the constant below for new pid driving system (deals with speeds instead of power)
DRIVE_MOTOR_POWER_MULTIPLIER = 25000
DRIVE_MIDDLE_WHEEL_SPEED = 1

#IDs for motors/physical components
# arbitrary numbers can put correct ones later
ID_DRIVE_FRONT_RIGHT = 1
ID_DRIVE_FRONT_LEFT = 2
ID_DRIVE_BACK_LEFT = 3
ID_DRIVE_BACK_RIGHT = 4

ID_ARM_EXTENSION = 12 # replacing elevator
ID_ARM_BASE = 8
ID_ARM_CLAW = 15

# not using the following three as of Battle of the Border (fall 2023)
ID_ARM_SERVO_CUBE = 0
ID_ARM_SERVO_CONE = 1
ID_ARM_CUBE_LIMIT_SWITCH = 0

ID_IMU_TALON = 11

ID_ADDITIONAL_FRONT = 10
ID_ADDITIONAL_BACK = 11

ID_ROTARY_CONTROLLER = 1
#ID_DRIVE_CONTROLLER = 1
ID_OPERATOR_CONTROLLER = 0

# BLUE = cube
# RED = cone
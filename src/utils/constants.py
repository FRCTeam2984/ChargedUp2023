# Enable/disable feature
ENABLE_DRIVING = True
ENABLE_ARM = True
ENABLE_BALANCE = True

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

# drive multipliers/power regulations
DRIVE_MOTOR_POWER_MULTIPLIER = 2
DRIVE_MIDDLE_WHEEL_SPEED = 3

# mode of autonomous can change/develop later
AUTO_MODE = 0

# stages of autonomous can change later
IDLE = 0
PLACING_PIECE = 1
MOVING_OUT_COMMUNITY = 2
TURNING = 3
BALANCING = 4
DONE = 5


#IDs for motors/physical components
# arbitrary numbers can put correct ones later
ID_DRIVE_FRONT_LEFT = 0
ID_DRIVE_FRONT_RIGHT = 1
ID_DRIVE_BACK_LEFT = 2
ID_DRIVE_BACK_RIGHT = 3

ID_DRIVE_MIDDLE_LEFT = 4
ID_DRIVE_MIDDLE_RIGHT = 5

ID_ARM_ELEVATOR = 6
ID_ARM_CHAIN = 7
ID_ARM_SERVO_1 = 8
ID_ARM_SERVO_2 = 9
ID_ARM_TOP_LIMIT_SWITCH = 0
ID_ARM_BOTTOM_LIMIT_SWITCH = 1

ID_ADDITIONAL_FRONT = 10
ID_ADDITIONAL_BACK = 11

ID_CONTROLLER = 1
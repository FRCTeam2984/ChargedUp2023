# Enable/disable feature
ENABLE_DRIVING = True
ENABLE_ARM = True
ENABLE_BALANCE = True

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

ID_CONTROLLER = 1
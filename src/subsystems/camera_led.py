from wpilib import PWM
from utils import math_functions

class Camera_LED:
   def __init__(self, _left_camera_led : PWM, _right_camera_led : PWM):
      self.left_camera_led = _left_camera_led
      self.right_camera_led = _right_camera_led

   def set_left_led(self, brightness):
      clamped_brightness = math_functions.clamp(brightness, 0, 255)
      self.left_camera_led.setRaw(clamped_brightness)

   def set_right_led(self, brightness):
      clamped_brightness = math_functions.clamp(brightness, 0, 255)
      self.right_camera_led.setRaw(clamped_brightness)

   def set_both_led(self, brightness):
      self.set_left_led(brightness)
      self.set_right_led(brightness)
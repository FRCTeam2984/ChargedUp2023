from rev import CANSparkMax, SparkMaxLimitSwitch

class Intake:
   def __init__(self, _intake_motor : CANSparkMax):
      self.intake_motor = _intake_motor

      self.cone_intake_speed = 0.75
      self.cube_intake_speed = 1
      self.outtake_speed = -1
      self.hold_speed = 0.15

      self.IDLE = 0
      self.HOLDING = 1
      self.INTAKING_CONE = 2
      self.INTAKING_CUBE = 3
      self.OUTTAKING = 4
      self.state = self.IDLE

   def idle(self):
      self.intake_motor.set(0)

   def hold(self):
      self.intake_motor.set(self.hold_speed)

   def intake_cube(self):
      self.intake_motor.set(self.cube_intake_speed)

   def intake_cone(self):
      self.intake_motor.set(self.cone_intake_speed)
   
   def outtake(self):
      self.intake_motor.set(self.outtake_speed)


   def update(self):
      if self.state == self.HOLDING:
         self.hold()

      elif self.state == self.INTAKING_CUBE:
         self.intake_cube()

      elif self.state == self.INTAKING_CONE:
         self.intake_cone()

      elif self.state == self.OUTTAKING:
         self.outtake()

      else:
         self.idle()

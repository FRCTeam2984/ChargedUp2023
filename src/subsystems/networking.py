#from networktables import NetworkTables
import ntcore

# Link to webcam option:
# https://www.amazon.com/Microphone-NexiGo-N980P-Reduction-Wide-Angle/dp/B08DHPBP65/ref=sr_1_3?keywords=wide+angle+webcam&qid=1674933445&sr=8-3

"""
network tables format:

cone_there = boolean
cone_x = int
cone_y = int
cone_ready = boolean
cone_angle = int
cone_is_upright = boolean

cube_there = boolean
cube_x = int
cube_y = int
cube_ready = boolean

each of these x2 with left or right
"""


class NetworkReciever:
   def __init__(self):
      self.instance = ntcore.NetworkTableInstance.getDefault()
      self.dashboard = self.instance.getTable("SmartDashboard")

# Greg: battery + breaker, radio + ethernet switch
# Kyle: Can BUS, drive train motors, assigning IDs and communicating with Aram
# Thomas and Aram: cooling Raspis, attaching Raspis, powering Raspis (ask about ordering second VRM to USB cable and how to female USB to USB-c)
# Any 2 mechanical people: Make side panels under the supports out of poly carbonate
# Zoe: wiring servos down to the ROBORio
# Everyone: Attaching large chain down the center of the robot

   def find_cube(self):
      cube_there = self.dashboard.getBoolean("cube_there", False)

      if cube_there:
         cube_x = self.dashboard.getNumber("cube_x", 0)
         cube_y = self.dashboard.getNumber("cube_y", 0) 
         counter = self.dashboard.getNumber("counter", -1)        

         return [True, cube_x, cube_y, counter]

   def find_cone(self):
      cone_there = self.dashboard.getBool("cone_there", False)

      if cone_there:
         cone_x = self.dashboard.getNumber("cone_x", 0)
         cone_y = self.dashboard.getNumber("cone_y", 0)

         cone_angle = self.dashboard.getNumber("cone_angle", 0)
         cone_is_upright = self.dashboard.getBoolean("cone_is_upright", False)

         return [True, cone_x, cone_y, cone_angle, cone_is_upright]

   def test(self):
      cube_there = self.dashboard.getBoolean("cube_there", False)

      counter = self.dashboard.getNumber("counter", 0)

      #print(f"sees cube = {cube_there}, counter = {counter}") 


# originally wrote using pynetworktables, but we need to use pyntcore
"""
class NetworkReceiver:
   def __init__(self):
      self.network_table_data = NetworkTables.getTable("SmartDashboard")

   
   def find_cubes(self):
      # sees if the raspberry pi that is sending the data has detected a cube
      # returns a boolean value (True/False) if it has detected anything
      # sets default value to False if nothing has been sent
      has_cube = self.network_table_data.getNumber("cube_detected", False)

      # gets x and y position of cube on the screen if cube has been detected
      # returns an integer from -200px to 200px based on the resulution of the camera
      if (has_cube):
         cube_x = self.network_table_data.getNumber("cube_x")
         cube_y = self.network_table_data.getNumber("cube_y")

         return [has_cube, cube_x, cube_y]


   def find_cones(self):
      # same thing as the above code but just for cones instead of cubes
      has_cone = self.network_table_data("cone_detected", False)

      if (has_cone):
         cone_x = self.network_table_data.getNumber("cone_x")
         cone_y = self.network_table_data.getNumber("cone_y")

         return [has_cone, cone_x, cone_y]

"""
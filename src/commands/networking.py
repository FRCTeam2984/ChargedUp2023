#from networktables import NetworkTables
import ntcore

# Link to webcam option:
# https://www.amazon.com/Microphone-NexiGo-N980P-Reduction-Wide-Angle/dp/B08DHPBP65/ref=sr_1_3?keywords=wide+angle+webcam&qid=1674933445&sr=8-3


class NetworkReciever:
   def __init__(self):
      self.instance = ntcore.NetworkTableInstance.getDefault()
      self.dashboard = self.instance.getTable("SmartDashboard")

   
   def find_cube(self):
      has_cube = self.dashboard.getBool("has_cube", False)

      if has_cube:
         cube_x = self.dashboard.getNumber("cube_x", 0)
         cube_y = self.dashboard.getNumber("cube_y", 0)


         return [has_cube, cube_x, cube_y]


   def find_cone(self):
      has_cone = self.dashboard.getBool("has_cone", False)

      if has_cone:
         cone_x = self.dashboard.getNumber("cone_x", 0)
         cone_y = self.dashboard.getNumber("cone_y", 0)

         return [has_cone, cone_x, cone_y]


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
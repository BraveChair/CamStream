import importlib
import sys
import os


class ExcludeModuleFinder(importlib.abc.MetaPathFinder):
    def __init__(self, exclude_module):
        self.exclude_module = exclude_module

    def find_spec(self, fullname, path, target=None):
        if fullname == self.exclude_module:
            raise ImportError(f"Module {self.exclude_module} is excluded.")
        return None

# add original to sys.path
sys.path.insert(0, os.path.abspath('/home/pi/test/CamStream/Pithermalcam/pithermalcam'))
# add custom to path
sys.path.insert(0, os.path.abspath('/home/pi/test/CamStream/set_up'))


# add the custom import hook to sys.meta_path
exclude_module = 'pithermalcam.pi_therm_cam'  # Replace with the module you want to exclude
sys.meta_path.insert(0, ExcludeModuleFinder(exclude_module))

# Now, attempt to import the library
try:
    import pithermalcam.pi_therm_cam
except ImportError as e:
    print(e)

# Import the rest of the library
import pithermalcam  # Import the rest of the library

# Test to see if the module is excluded
try:
    import pithermalcam.pi_therm_cam
except ImportError as e:
    print("Successfully excluded module:", e)

# Use your custom module in place of the excluded one
import your_custom_pi_therm_cam as pi_therm_cam

# Rest of your code
# Now you can use pi_therm_cam instead of pithermalcam.pi_therm_cam

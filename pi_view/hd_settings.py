
from picamera2 import Picamera2, Preview
import time
from pprint import *
from pynput import keyboard

picam2 = Picamera2()
camera_running = False
config = picam2.create_preview_configuration()
picam2.confingure(config)

# config = picam2.create_preview_configuration()
# main: Any = {},
# lores: Any | None = None,
# raw: Any = {},
# transform: Any = libcamera.Transform(),
# colour_space: Any = libcamera.ColorSpace.Sycc(),
# buffer_count: int = 4,
# controls: Any = {},
# display: str = "main",
# encode: str = "main",
# queue: bool = True,
# sensor: Any = {},
# use_case: str = "preview"
# {'use_case': 'preview', 
# 'transform': <libcamera.Transform 'identity'>, 
# 'colour_space': <libcamera.ColorSpace 'sYCC'>, 
# 'buffer_count': 4, 
# 'queue': True, 
# 'main': {'format': 'XBGR8888', 'size': (640, 480)}, 
# 'lores': None, 
# 'raw': {'format': 'SRGGB12_CSI2P', 'size': (640, 480)}, 

# 'controls': {'NoiseReductionMode': <NoiseReductionModeEnum.Minimal: 3>, 
# 			'FrameDurationLimits': (100, 83333)}, 'sensor': {}, 
# 		'display': 'main', 'encode': 'main'}




      

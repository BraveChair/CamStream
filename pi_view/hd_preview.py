
from picamera2 import Picamera2, Preview
# import libcamera
import time
from pprint import *
import keyboard
import os
import io
import cv2
import numpy as np
#from hd_settings import config


global camera_running
global picam2
global preview_on
global configured
global i
i = 0


picam2 = Picamera2()
camera_running = False
preview_on = False
configured = False
config = picam2.create_preview_configuration()

save_directory = '/home/raspi/test/brave_repo/chessboard/hd_images'


def hd_cam_off():
	global i, camera_running, picam2, preview_on
	if preview_on == True:
		picam2.stop_preview()
		preview_on = False
		camera_running = True


def hd_cam_on():
	global i, camera_running, picam2, configured, preview_on
	if configured == False:
		picam2.configure(config)
		configured = True
		time.sleep(1)

	if preview_on == False:
		picam2.start_preview(Preview.QTGL)
		preview_on = True

	if camera_running == False:
		picam2.start()
		camera_running = True
	i = 1

def toggle_cam():
	global i, camera_running, picam2, preview_on, configured, config
	try:
		if configured == False:
			picam2.configure(config)
			configured = True
			time.sleep(1)

		#turn on		
		if i == 0:
			hd_cam_on()
			return
			
		elif i == 1:
			hd_cam_off()
			i = 0
			return

		else:
			print(f"i Error")
			return

	except RuntimeError as e:
		camera_running == True
		print(f"Error: {e}")
		if preview_on == True:
			picam2.stop_preview()
		picam2.stop()

def hd_settings():
	global camera_running, picam2, preview_on,configured,config

	try: 
		if configured:
			print(config['main'])
		else:
			print("Configuring...")
			picam2.configure(config)
			configuration = True
			time.sleep(1)
			print(config['main'])

		command = input("Press 'm' to view possible modes or hit 'b' to go back").strip().lower()
		if command == 'm':
			if camera_running or preview_on:
				if preview_on:
					picam2.stop_preview()
					preview_on = False
				elif camera_running:
					picam2.stop()
					camera_running = False
				time.sleep(1)
				pprint(picam2.sensor_modes)	
				
			else:
				time.sleep(1)
				pprint(picam2.sensor_modes)

		elif command == 'b' or 'esc':
			return
		
		else:
			print("Wrong input, try 'm' to view possible modes or 'b' to go back")

	except RuntimeError as e:
		camera_running == True
		print(f"Error: {e}")
		if preview_on == True:
			picam2.stop_preview()
		picam2.stop()

def capture_image():

	# find amount of files in folder and name new pic in succsession
	f = os.listdir(save_directory)
	current_number = len(f) +1
	filename = save_directory + "/no" + str(current_number) +".jpg"
	
	#set up for capture
	capture_config = picam2.create_still_configuration(main={"size":(2078,1520)})
	picam2.switch_mode_and_capture_file(capture_config, filename)
	
	# need to crop image size to managable level
	
	print("YAY GO HOME")
	print('Image saved to: ',filename)


def exit():
	global i, camera_running, picam2, preview_on
	print(" Exiting")
	if preview_on == True:
		picam2.stop_preview()
	picam2.stop()
	picam2.close()

	
def main():
	global camera_running
	global picam2
	global preview_on
	global configured
	global config
	c = False
	while True:
		command = input("Enter 'c' to toggle camera, 'p' to capture picture, 's' for settings, 'q' to quit: ").strip().lower()
		if command == 'c':
			toggle_cam()
			c = True

		elif command == 'p':
			if c == False:
				toggle_cam()
			time.sleep(1)
			capture_image()
						
		elif command == 's':
			hd_settings()
			
		elif command == 'q' or KeyboardInterrupt: 
			exit()
			break

		# elif command not in ['c', 'p', 's','q', KeyboardInterrupt]:
		# 	print("Wrong input, try 'c' to toggle, 's' see setting, or 'q' to quit")




if __name__ == "__main__":
	main()
	

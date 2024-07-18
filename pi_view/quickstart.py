
from picamera2 import Picamera2, Preview
import time
from pprint import *
from pynput import keyboard

picam2 = Picamera2()
camera_running = False
config = picam2.create_preview_configuration()
picam2.confingure(config)
picam2.start()
picam2.start_preview(Preview.QTGL)
print("Enter 'q' to quit: ")
command = input("Press 'm' to view possible modes or hit 'b' to go back").strip().lower()

def main():
    if command == 'q' or KeyboardInterrupt:
        print("Exiting ")
        picam2.stop_preview()
        picam2.stop()

if __name__ == "__main__":
    main()

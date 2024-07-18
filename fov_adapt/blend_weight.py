
import cv2
from picamera2 import Picamera2, Preview
import pithermalcam as ptc
import time
from pprint import *
import keyboard

def _show_processed_image(ptc):
        """Resize image window and display it"""
        cv2.namedWindow('Thermal Image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Thermal Image', ptc.image_width,ptc.image_height)
        cv2.imshow('Thermal Image', ptc._image)

        output_folder = '/home/pi/PiThermalCam/saved_snapshots/'
        thermcam = ptc(output_folder=output_folder) 

def blend_images(picam2_image, thermal_image):
    """Blend two images"""
    picam2_image = cv2.cvtColor(picam2_image, cv2.COLOR_RGB2BGR)

    if thermal_image.shape != picam2_image.shape:
        thermal_image = cv2.resize(thermal_image, (800, 600))
        picam2_image = cv2.resize(picam2_image, (800, 600))
    
    # Use cv2.addWeighted to blend the images
    alpha = 0.5  # weight for the first image
    beta = 1.0 - alpha  # weight for the second image
    blended_image = cv2.addWeighted(thermal_image, alpha, picam2_image, beta, 0)

    return blended_image

def main():
    cv2.namedWindow("Combined_feed",cv2.WINDOW_NORMAL)
    # using cv2.imshow() to display the image 
    cv2.imshow('Display', blended_image) 
    
    # Waiting 0ms for user to press any key 
    cv2.waitKey(0) 
    
    # Using cv2.destroyAllWindows() to destroy 
    # all created windows open on screen 
    cv2.destroyAllWindows() 
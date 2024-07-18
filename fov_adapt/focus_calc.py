import cv2
import numpy as np
import time
import os
from picamera2 import Picamera2, Preview



def focusing(val):
    value = (val << 4) & 0x3ff0
    data1 = (value >> 8) & 0x3f
    data2 = value & 0xf0
    print("Focus value: {}".format(val))
    # comment the line below if not using i2cset to control focus
    os.system("i2cset -y 0 0x0c %d %d" % (data1, data2))

def laplacian(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_laplacian = cv2.Laplacian(img_gray, cv2.CV_16U)
    return cv2.mean(img_laplacian)[0]

def calculate_focus(hd_cam):
    image = hd_cam.capture_array()
    return laplacian(image)

def estimate_distance(focus_value):
    # assuming focus_value is proportional to distance.
    # should be replaced based on calibration.
    min_distance = 0.3  # Minimum object distance (MOD) in meters
    max_distance = 10.0  # Assumed maximum distance for this example
    distance = min_distance + (1000 - focus_value) * (max_distance - min_distance) / 1000
    return distance

def main(): #CHECK WITH SERVER sensor size?
    # Initialize Picamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"Size":(640, 480)})
    picam2.configure(config)
    picam2.start()

    # preview (if needed)
    # picam2.start_preview(Preview.NULL) #
    picam2.set_controls({"Resolution": (640, 480)})
    time.sleep(0.1)
    print("Start focusing")

    focal_distance = 10 #starting value, adjust
    max_index = 10 
    max_value = 0.0
    last_value = 0.0
    dec_count = 0
    

    # create window for video feed
    cv2.namedWindow("Stream", cv2.WINDOW_NORMAL)

    try:
        while True:
            #adjust focus
            focusing(focal_distance)
            time.sleep(0.5)  # allow for focus adjustment

            #capture + calculate image clarity
            val = calculate_focus(picam2)

            #find the max image clarity
            if val > max_value:
                max_index = focal_distance
                max_value = val

            # check if image clarity starts to decrease
            if val < last_value:
                dec_count += 1
            else:
                dec_count = 0

            # clarity -6 consecutive frames = stop
            if dec_count > 6:
                break

            last_value = val

            # increase focal distance
            focal_distance += 15
            if focal_distance > 1000:
                break

        # adjust focus to best
        focusing(max_index)
        time.sleep(1)  # allow for focus adjustment

        # estimate the distance based on the best focus value
        distance = estimate_distance(max_index)
        print(f"Estimated distance: {distance:.2f} units")

        # Set camera resolution to 1920x1080
        picam2.set_controls({"Resolution": (1920, 1080)})

        # main loop for constant distance calculation
        while True:
            # capture the current frame
            frame = picam2.capture_array()

            # calculate focus value
            val = calculate_focus(picam2)
            distance = estimate_distance(val)
            
            # print distance in  terminal
            print(f"Current estimated distance: {distance:.2f} units")

            # Display frame in window
            cv2.imshow("Stream", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

            # Exit streaming loop on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # cleanup
        picam2.stop_preview()
        picam2.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

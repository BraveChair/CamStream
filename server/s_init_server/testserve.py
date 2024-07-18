

from flask import Flask, Response, render_template
import threading
import time
import io
import cv2
from picamera2 import Picamera2
try:
    from pithermalcam import pithermalcam
except ImportError:
    from pi_therm_cam import pithermalcam

app = Flask(__name__)

# Global variables for HD and Thermal camera frames
hd_output_frame = None
thermal_output_frame = None
hd_lock = threading.Lock()
thermal_lock = threading.Lock()

# Define the desired crop dimensions
CROP_WIDTH = 550
CROP_HEIGHT = 280

# HD Camera Thread and Functionality
def capture_hd_frames():
    global hd_output_frame, hd_lock
    picam2_hd = Picamera2()
    config_hd = picam2_hd.create_preview_configuration(main={"size": (640, 480)})
    picam2_hd.configure(config_hd)
    picam2_hd.start()

    while True:
        try:
            image_hd = picam2_hd.capture_array()
            height, width, channels = image_hd.shape
            start_x = (width - CROP_WIDTH) // 2
            start_y = (height - CROP_HEIGHT) // 2
            cropped_hd_image = image_hd[start_y:start_y+CROP_HEIGHT, start_x:start_x+CROP_WIDTH]
            cropped_hd_image = cv2.cvtColor(cropped_hd_image, cv2.COLOR_BGR2RGB)
            with hd_lock:
                hd_output_frame = cropped_hd_image.copy()
        except Exception as e:
            print(f"Error capturing HD frame: {e}")

# Thermal Camera Thread and Functionality
def pull_images():
    global thermal_output_frame, thermal_lock
    thermcam = pithermalcam(output_folder='/home/pi/pithermalcam/saved_snapshots/')
    time.sleep(0.1)

    while True:
        try:
            current_frame = thermcam.update_image_frame()
            if current_frame is not None:
                with thermal_lock:
                    thermal_output_frame = current_frame.copy()
        except Exception as e:
            print(f"Error capturing thermal frame: {e}")

# Flask Routes
@app.route("/")
def index():
    return render_template("index.html")

def generate():
    global hd_output_frame, thermal_output_frame, hd_lock, thermal_lock
    while True:
        with hd_lock:
            hd_frame = hd_output_frame.copy() if hd_output_frame is not None else None
        with thermal_lock:
            thermal_frame = thermal_output_frame.copy() if thermal_output_frame is not None else None

        if hd_frame is None or thermal_frame is None:
            continue

        # Resize frames if needed to display side by side
        hd_frame = cv2.resize(hd_frame, (320, 240))
        thermal_frame = cv2.resize(thermal_frame, (320, 240))

        # Combine frames horizontally
        combined_frame = cv2.hconcat([hd_frame, thermal_frame])

        # Encode combined frame
        (flag, encoded_image) = cv2.imencode(".jpg", combined_frame)
        if not flag:
            continue

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encoded_image) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    # Start HD camera thread
    hd_thread = threading.Thread(target=capture_hd_frames)
    hd_thread.daemon = True
    hd_thread.start()

    # Start Thermal camera thread
    thermal_thread = threading.Thread(target=pull_images)
    thermal_thread.daemon = True
    thermal_thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=8010, debug=True, threaded=True, use_reloader=False)



from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import time
import cv2
import numpy as np
import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from picamera2 import Picamera2
try: # If called as an imported module
    from pithermalcam import pithermalcam
except: # If run directly
    from pi_therm_cam import pithermalcam

app = Flask(__name__)
socketio = SocketIO(app)

hd_output_frame = None
thermal_output_frame = None
hd_lock = threading.Lock()
thermal_lock = threading.Lock()

# Crop dimensions
CROP_WIDTH = 550
CROP_HEIGHT = 280

# WebRTC setup
pcs = set()

class VideoStreamTrack(MediaStreamTrack):
    def __init__(self, video_source):
        super().__init__()  # Initialize base class
        self.video_source = video_source

    async def recv(self):
        # Capture and process the frame
        if self.video_source == 'hd':
            with hd_lock:
                frame = hd_output_frame.copy() if hd_output_frame is not None else None
        elif self.video_source == 'thermal':
            with thermal_lock:
                frame = thermal_output_frame.copy() if thermal_output_frame is not None else None

        if frame is None:
            return None

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Convert to the format needed by WebRTC
        frame = np.array(frame)
        return frame

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/offer", methods=["POST"])
async def offer():
    data = request.json
    offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
    
    pc = RTCPeerConnection()
    pcs.add(pc)

    # Add video tracks
    pc.addTrack(VideoStreamTrack('hd'))
    pc.addTrack(VideoStreamTrack('thermal'))

    @pc.on("icecandidate")
    async def on_icecandidate(candidate):
        if candidate:
            await pc.addIceCandidate(candidate)

    @pc.on("track")
    def on_track(track):
        print("Track received")

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return jsonify({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})

@app.route("/disconnect")
async def disconnect():
    for pc in pcs:
        await pc.close()
    pcs.clear()
    return "Disconnected"

def capture_hd_frames():
    global hd_output_frame, hd_lock
    picam2_hd = Picamera2()
    config_hd = picam2_hd.create_preview_configuration(main={"size": (640, 480)})
    picam2_hd.configure(config_hd)
    picam2_hd.start()

    while True:
        image_hd = picam2_hd.capture_array()
        height, width, channels = image_hd.shape
        start_x = (width - CROP_WIDTH) // 2
        start_y = (height - CROP_HEIGHT) // 2
        cropped_hd_image = image_hd[start_y:start_y+CROP_HEIGHT, start_x:start_x+CROP_WIDTH]
        cropped_hd_image = cv2.cvtColor(cropped_hd_image, cv2.COLOR_BGR2RGB)
        with hd_lock:
            hd_output_frame = cropped_hd_image.copy()

def pull_images():
    global thermal_output_frame, thermal_lock
    thermcam = pithermalcam(output_folder='/home/pi/pithermalcam/saved_snapshots/')
    time.sleep(0.1)

    while True:
        current_frame = thermcam.update_image_frame()
        if current_frame is not None:
            with thermal_lock:
                thermal_output_frame = current_frame.copy()

if __name__ == '__main__':
    hd_thread = threading.Thread(target=capture_hd_frames)
    hd_thread.daemon = True
    hd_thread.start()

    thermal_thread = threading.Thread(target=pull_images)
    thermal_thread.daemon = True
    thermal_thread.start()

    socketio.run(app, host='0.0.0.0', port=8010, debug=True, use_reloader=False)

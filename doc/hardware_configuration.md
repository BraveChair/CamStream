# Hardware Configuartion for IMX477

1. Locate the camera connector (CSI). It’s on the side of the carrier board, opposite to the GPIO pins.

2. Pull up on the plastic edges of the camera port. Do it gently to avoid pulling it off.

3. Push in the camera ribbon. Make sure the contacts are facing the heatsinks. Do not bend the flex cable, and make sure it’s firmly inserted into the bottom of the connector.

# Software Configuration for IMx477

1. For Raspberry Pi Bookworm/Bullseye users running on Pi 4, please execute: 

> sudo nano /boot/firmware/config.txt 
>#Find the line: camera_auto_detect=1, update it to:
>camera_auto_detect=0
>#Find the line: [all], add the following item under it:
>dtoverlay=imx477
>#Save and reboot.

2. Navigate to the termial and run the command:

>libcamera-still -t0


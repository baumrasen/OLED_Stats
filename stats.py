# Created by: Michael Klements
# For Raspberry Pi Desktop Case with OLED Stats Display
# Base on Adafruit CircuitPython & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
#
# Changed to use luma.oled
# pip install luma.oled
#
# start with (for example) 
# python3 stats.py -d sh1106 -r 2
# 
# get help with start parameter
# python3 stats.py -h

import time
import subprocess

from luma.core.render import canvas
from luma_opts import get_device
from PIL import Image, ImageFont

## rotate: An integer value of 0 (default), 1, 2 or 3 only, where 0 is
##        no rotation, 1 is rotate 90° clockwise, 2 is 180° rotation and 3
##        represents 270° rotation.
#oled = sh1106(serial, rotate=2)
oled = get_device()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

font = ImageFont.truetype('PixelOperator.ttf', 16)
#font = ImageFont.load_default()

while True:
  with canvas(oled) as draw:

    # Draw a white background
    draw.rectangle(oled.bounding_box, outline=255, fill=255)

    # Draw a black filled box to clear the image.
    draw.rectangle(oled.bounding_box, outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell = True )

    # Pi Stats Display
    draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=font, fill=255)
    draw.text((0, 16), str(CPU,'utf-8') + "%", font=font, fill=255)
    draw.text((80, 16), str(temp,'utf-8') , font=font, fill=255)
    draw.text((0, 32), str(MemUsage,'utf-8'), font=font, fill=255)
    draw.text((0, 48), str(Disk,'utf-8'), font=font, fill=255)

    # slow for low cpu usage
    time.sleep(5)

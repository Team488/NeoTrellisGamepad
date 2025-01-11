 # requires the adafruit_hid, adafruit_neotrellis, adafruit_matrixkeypad.mpy, adafruit_tellism4.mpy, and neopixel.mpy libraries.

import time
import adafruit_trellism4
import struct
from adafruit_hid import find_device
from hid_gamepad import Gamepad
import usb_hid
from builtins import set

trellis = adafruit_trellism4.TrellisM4Express()

gp = Gamepad(usb_hid.devices)


# Change the overall brightness of the NeoTrellis
trellis.pixels.brightness = 1.0

def setButtonColor(button, color):
    x = (button - 1) % 8
    y = (button - 1) // 8
    trellis.pixels[x, y] = color

print ("program starting")

# Set button 1 to (R, G, B) color 0, 0, 128
# setButtonColor(1, (0, 0, 128))

# pressed_buttons returns the set of pressed buttons
# buttons are numbered from 1 to 32
#
# |———————————————————————————————|
# | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
# |———————————————————————————————|
# | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
# |———————————————————————————————|
# | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
# |———————————————————————————————|
# | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 |
# |———————————————————————————————|

# 1, 10, 19, 28, 21, 14, 7, 16, 23,30, 21, 12, 3, 10, 17, 26, 19, 12, 5, 14, 23, 32
buttonstolight=set()
buttonspressedlastloop=set()

while True:
    pressed = trellis.pressed_keys
    if pressed:
        pressed_buttons = [(x + y * 8) + 1 for x, y in pressed]
        for pressedbutton in pressed_buttons:
            if pressedbutton in buttonstolight and pressedbutton not in buttonspressedlastloop:
                buttonstolight.remove(pressedbutton)
            elif pressedbutton not in buttonstolight and pressedbutton not in buttonspressedlastloop:
                buttonstolight.add(pressedbutton)
        print("Pressed buttons:", pressed_buttons)
        print("buttonstolight:", buttonstolight)
        print ("buttonspressedlastloop", buttonspressedlastloop)
        buttonspressedlastloop=pressed_buttons
    else:
        buttonspressedlastloop=set()


# Render loop
    for buttonindex in range(1,32):
        color=(0,0,0)
        if buttonindex in buttonstolight:
            color=(255,0,0)
        setButtonColor(buttonindex,color)
    time.sleep(0.001)
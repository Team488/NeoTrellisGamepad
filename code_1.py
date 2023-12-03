# requires the adafruit_hid, adafruit_neotrellis, adafruit_matrixkeypad.mpy, adafruit_tellism4.mpy, and neopixel.mpy libraries.

import time
import adafruit_trellism4
import struct
from adafruit_hid import find_device
from hid_gamepad import Gamepad
import usb_hid

trellis = adafruit_trellism4.TrellisM4Express()

gp = Gamepad(usb_hid.devices)
gp.press_buttons(2)

"""
while True:
    trellis.pixels[0, 0] = (0, 0, 0)
    gp.press_buttons(2)
    time.sleep(0.5)
    trellis.pixels[0, 0] = (0, 0, 0)
    gp.release_buttons(2)
    time.sleep(0.5)
"""


while True:
    pressed = trellis.pressed_keys
    if pressed:
        pressed_buttons = []
        for x, y in pressed:
            button = (x + y * 8) + 1
            pressed_buttons.append(button)
            trellis.pixels[x, y] = (255, 0, 0)  # Set pressed buttons to red
        print("Pressed buttons:", pressed_buttons)
        gp.press_buttons(*pressed_buttons)
        for i in range(1, 17):
            if i not in pressed_buttons:
                gp.release_buttons(i)
                trellis.pixels[(i - 1) % 8, (i - 1) // 8] = (0, 0, 0)  # Set released buttons to black
    else:
        gp.release_all_buttons()
        trellis.pixels.fill((0, 0, 0))  # Set all buttons to black
    time.sleep(0.001)
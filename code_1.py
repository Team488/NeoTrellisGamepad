# requires the adafruit_hid, adafruit_neotrellis, adafruit_matrixkeypad.mpy, adafruit_tellism4.mpy, and neopixel.mpy libraries.

import time
import adafruit_trellism4
import struct
from adafruit_hid import find_device
from hid_gamepad import Gamepad
import usb_hid

trellis = adafruit_trellism4.TrellisM4Express()

gp = Gamepad(usb_hid.devices)

while True:
    pressed = trellis.pressed_keys
    if pressed:
        pressed_buttons = []
        for x, y in pressed:
            button = (x + y * 8) + 1
            pressed_buttons.append(button)
        print("Pressed buttons:", pressed_buttons)
        gp.press_buttons(*pressed_buttons)
        for i in range(1, 17):
            if i not in pressed_buttons:
                gp.release_buttons(i)
    else:
        gp.release_all_buttons()
    for x in range(0, 7):
        for y in range(0, 3):
            if gp.led_on((x + y * 8)):
                trellis.pixels[(x, y)] = (255, 0, 0)
            else:
                trellis.pixels[(x, y)] = (0, 0, 0)
    time.sleep(0.001)
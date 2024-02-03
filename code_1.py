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

# Change the overall brightness of the NeoTrellis
trellis.pixels.brightness = 0.1

def getDefaultButtonColor(button):
    # buttons 2,3,4,5,6 are orange, representing midline notes
    # buttons 10, 11, 12 are orange, representing spike notes.
    # button 14 is a bright purple, representing the Source.
    # buttons 17, 18, and 19 are dim white, representing ranged shots.
    # buttons 25, 26, 27 are bright green, representing melee shots.
    # button 9 is bright blue, representing the Amp.

    if button in [2, 3, 4, 5, 6, 10, 11, 12]:
        return (255, 128, 0)
    elif button in [17, 18, 19]:
        return (128, 128, 128)
    elif button in [25, 26, 27]:
        return (0, 255, 0)
    elif button == 14:
        return (128, 0, 128)
    elif button == 9:
        return (0, 0, 255)
    else:
        return (0, 0, 0)

def setButtonColor(button, color):
    x = (button - 1) % 8
    y = (button - 1) // 8
    trellis.pixels[x, y] = color

def setAllButtonsBackToDefault():
    for i in range(1, 33):
        setButtonColor(i, getDefaultButtonColor(i))

# Initially loop through all 32 buttons and set their colors to the default colors.
setAllButtonsBackToDefault()

# Now, respond dynamically to button presses.

# Initialize a set to keep track of the pressed buttons
pressed_buttons_set = set()

# Initialize the last_pressed_buttons list
last_pressed_buttons = []

while True:
    pressed = trellis.pressed_keys
    if pressed:
        pressed_buttons = [(x + y * 8) + 1 for x, y in pressed]
        for x, y in pressed:
            trellis.pixels[x, y] = (255, 0, 0)  # Set pressed buttons to red
        print("Pressed buttons:", pressed_buttons)
        gp.press_buttons(*pressed_buttons)

        pressed_buttons_set.update(pressed_buttons)

        for button in last_pressed_buttons:
            if button not in pressed_buttons:
                setButtonColor(button, getDefaultButtonColor(button))
                if button in pressed_buttons_set:
                    gp.release_buttons(button)
                    pressed_buttons_set.discard(button)
        last_pressed_buttons = pressed_buttons        
    else:
        gp.release_all_buttons()
        pressed_buttons_set.clear()

        for button in last_pressed_buttons:
            setButtonColor(button, getDefaultButtonColor(button))
        
        last_pressed_buttons = []
        
    time.sleep(0.001)
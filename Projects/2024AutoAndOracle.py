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
trellis.pixels.brightness = 0.1

meleeScoring = set([26,27,28])
rangedScoring = set([17,18,19,20])
spikeNotes = set([10,11,12])
midlineNotes = set([2,3,4,5,6])
reservedButtons = set([1,9,25])
breadAndButter = set([23])
oracleAuto = set([31])
breadAndButterExtended = set([16])

# autoButtons are the set of buttons (out of 32 possible) not in any of the above sets.
autoButtons = set(range(1,33)) - (meleeScoring | rangedScoring | spikeNotes | midlineNotes | reservedButtons | breadAndButter | oracleAuto | breadAndButterExtended)

def getDefaultButtonColor(button):
    # buttons 2,3,4,5,6 are orange, representing midline notes
    # buttons 10, 11, 12 are orange, representing spike notes.
    # buttons 18, 19, and 20 are dim white, representing ranged shots.
    # buttons 25, 26, 27 are bright green, representing melee shots.

    if button in spikeNotes or button in midlineNotes:
        return (255, 128, 0)
    elif button in rangedScoring:
        return (128, 128, 128)
    elif button in meleeScoring:
        return (0, 255, 0)
    elif button in autoButtons:
        return (0, 0, 255)
    elif button in breadAndButter:
        return (128,0,128)
    elif button in oracleAuto:
        return (128, 0, 0)
    elif button in breadAndButterExtended:
        return (255,255,255)
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

toggled_active_buttons = set()

special_toggle_buttons = set()
special_toggle_buttons.update(spikeNotes)
special_toggle_buttons.update(midlineNotes)
special_toggle_buttons.update(meleeScoring)
special_toggle_buttons.update(rangedScoring)

# general pattern:
# Check for any pressed buttons.

#   If there are any pressed buttons, see if they are members of the special set of toggle buttons (2-6, 10-12, 25-27).
#   If they are, see if they were pressed last loop. If so, take no action. But if they are new:
#        If they are not in the set of toggled_active_buttons, add them.
#        If they are in the set of toggled_active_buttons, remove them.
#   Then, for each button in the set of toggled_active_buttons, press the button on the gamepad.

#   If they are not members of the special set of toggle buttons, then:
#        Press the matching button on the gamepad
#        Set that button to red color

#    If there are any buttons that were pressed last loop but are not pressed this loop, release them on the gamepad and set their color back to the default color.

while True:
    pressed = trellis.pressed_keys
    if pressed:
        pressed_buttons = [(x + y * 8) + 1 for x, y in pressed]
        #for x, y in pressed:
        #    trellis.pixels[x, y] = (255, 0, 0)  # Set pressed buttons to red
        print("Pressed buttons:", pressed_buttons)
        
        for currentButton in pressed_buttons:
            if currentButton in special_toggle_buttons:
                if currentButton not in last_pressed_buttons: #checking for special button and debouncing
                    if currentButton in toggled_active_buttons:
                        toggled_active_buttons.remove(currentButton)
                        gp.release_buttons(currentButton)
                        setButtonColor(currentButton, getDefaultButtonColor(currentButton))
                    else:
                        toggled_active_buttons.add(currentButton)
                        gp.press_buttons(currentButton)
                        setButtonColor(currentButton, (255, 0, 0))
            else:
                # this is a boring regular button
                setButtonColor(currentButton, (255, 0, 0))
                gp.press_buttons(currentButton)
        print("Toggled active buttons:", toggled_active_buttons)
        # Keep track of what buttons are pressed for the next cycle
        pressed_buttons_set.clear()
        pressed_buttons_set.update(pressed_buttons)

        # Release any regular buttons that were pressed last loop but are not pressed this loop
        for button in last_pressed_buttons:
            if button not in pressed_buttons and button not in special_toggle_buttons:
                setButtonColor(button, getDefaultButtonColor(button))
                gp.release_buttons(button)
        last_pressed_buttons = pressed_buttons        
    else:
        #gp.release_all_buttons()
        pressed_buttons_set.clear()

        for button in last_pressed_buttons:
            if button not in special_toggle_buttons:
                gp.release_buttons(button)
                setButtonColor(button, getDefaultButtonColor(button))
        
        last_pressed_buttons = []
        
    time.sleep(0.001)
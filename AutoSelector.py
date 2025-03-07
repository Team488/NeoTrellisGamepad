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

lightgreenset=set()
lightpinkset=set()
lightorangeset=set()
print ("program starting")

# Set button 1 to (R, G, B) color 0, 0, 128
# setButtonColor(1, (0, 0, 128))

#pressed_buttons returns the set of pressed buttons
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

pink_Array=(9,10,17,18)
orange_Array=(12,13,20,21)
green_Array=(15,16,23,24)
for buttonindex in pink_Array:
    setButtonColor(buttonindex,(40,8,20))
for buttonindex in orange_Array:
    setButtonColor(buttonindex,(40,25,0))
for buttonindex in green_Array:
    setButtonColor(buttonindex,(25,40,0))
while True:
    pressed = trellis.pressed_keys
    if pressed:
        pressed_buttons = [(x + y * 8) + 1 for x, y in pressed]
        for pressedbutton in pressed_buttons:
            #FACECOLORS
            if pressedbutton in pink_Array:
                for pinkbutton in pink_Array:
                    lightpinkset.add(pinkbutton)
            if pressedbutton in orange_Array:
                for orangebutton in orange_Array:
                    lightorangeset.add(orangebutton)
            if pressedbutton in green_Array:
                    for greenbutton in green_Array:
                        lightgreenset.add(greenbutton)

    for buttonindex in range(1,33):
        #FACECOLORS
        for buttons in lightpinkset:
            setButtonColor(buttons,(197,85,90))
        for buttons in lightorangeset:
            setButtonColor(buttons,(130,85,0))
        for buttons in lightgreenset:
            setButtonColor(buttons,(85,130,0))

    time.sleep(0.0001)

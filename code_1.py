# requires the adafruit_hid, adafruit_neotrellis, adafruit_matrixkeypad.mpy, adafruit_tellism4.mpy, and neopixel.mpy libraries.

import time
import adafruit_trellism4
import struct
from adafruit_hid import find_device
from hid_gamepad import Gamepad
import usb_hid
import usb_cdc

trellis = adafruit_trellism4.TrellisM4Express()

serial = usb_cdc.data
gp = Gamepad(usb_hid.devices)

if serial is None:
    print("No serial connection!")
else:
    print("Serial present")
    serial.timeout = 0.1

def clearLeds(trellis):
    trellis.pixels.fill(0)

def inRange(value, min, max):
    return value >= min and value <= max

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
    if serial.connected:
        while serial.in_waiting >= 12:
            # Serial byte packed format: LLRRRGGGBBB\n
            # LL: Led number
            # RRR: Red intensity
            # GGG: Green intensity
            # BBB: Blue intensity
            command = serial.readline()
            if command is None:
                break
            if (len(command)) != 12:
                print("Unexpected command length: ", len(command))
                clearLeds(trellis)
                serial.reset_input_buffer()
                continue
            commandString = str(command[:11], 'ascii')
            print("Received command:", str(commandString))

            if not commandString.isdigit():
                print("Not a numeric command. Clearing!")
                clearLeds(trellis)
                continue

            ledNumber = int(commandString[:2])
            redValue = int(commandString[2:5])
            greenValue = int(commandString[5:8])
            blueValue = int(commandString[8:11])
            if not inRange(ledNumber, 1, 32):
                print("Unexpected led number:", ledNumber)
                continue
            if not inRange(redValue, 0, 255):
                print("Unexpected red value:", redValue)
                continue
            if not inRange(greenValue, 0, 255):
                print("Unexpected green value:", greenValue)
                continue
            if not inRange(blueValue, 0, 255):
                print("Unexpected blue value:", blueValue)
                continue
            
            x = (ledNumber-1) % 8
            y = int((ledNumber-1) // 8)
            trellis.pixels[(x, y)] = (redValue, greenValue, blueValue)
    else:
        print("Serial not connected")
    time.sleep(0.001)

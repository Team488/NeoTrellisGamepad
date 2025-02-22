# requires the adafruit_hid, adafruit_neotrellis, adafruit_matrixkeypad.mpy, adafruit_tellism4.mpy, and neopixel.mpy libraries.

import time
import adafruit_trellism4
from hid_gamepad import Gamepad
import usb_hid

# Initialize Trellis and Gamepad
neo_trellis = adafruit_trellism4.TrellisM4Express()
gamepad = Gamepad(usb_hid.devices)

# Set brightness
neo_trellis.pixels.brightness = 0.1

# Button mappings
button_mappings = {
    1: (0, 0), 2: (1, 0), 3: (2, 0), 4: (3, 0), 5: (4, 0), 6: (5, 0), 7: (6, 0), 8: (7, 0),
    9: (0, 1), 10: (1, 1), 11: (2, 1), 12: (3, 1), 13: (4, 1), 14: (5, 1), 15: (6, 1), 16: (7, 1),
    17: (0, 2), 18: (1, 2), 19: (2, 2), 20: (3, 2), 21: (4, 2), 22: (5, 2), 23: (6, 2), 24: (7, 2),
    25: (0, 3), 26: (1, 3), 27: (2, 3), 28: (3, 3), 29: (4, 3), 30: (5, 3), 31: (6, 3), 32: (7, 3)
}

# Default colors
location_buttons = {2, 3, 4, 5, 9, 14, 17, 22, 26, 27, 28, 29}
level_buttons = {8, 16, 24, 32}
special_buttons = {11, 19, 20}

# Assign colors to ReefFace buttons
reef_face_colors = {
    (27, 28): (0, 255, 0),  # Green
    (29, 22): (0, 0, 255),  # Blue
    (14, 5): (255, 0, 0),   # Red
    (4, 3): (255, 255, 0),  # Yellow
    (2, 9): (255, 0, 255),  # Magenta
    (17, 26): (0, 255, 255) # Cyan
}

# Set default colors
button_colors = {}
for button, (x, y) in button_mappings.items():
    if button in location_buttons or button in level_buttons:
        color = (0, 0, 255)  # Blue
    elif button in special_buttons:
        color = (255, 255, 255)  # White
    else:
        color = (0, 0, 0)  # No color
    neo_trellis.pixels[x, y] = color
    button_colors[button] = color

# Override colors for ReefFace buttons
for buttons, color in reef_face_colors.items():
    for button in buttons:
        x, y = button_mappings[button]
        neo_trellis.pixels[x, y] = color
        button_colors[button] = color

# Track pressed buttons
pressed_buttons = set()

while True:
    current_pressed = set((x + y * 8 + 1) for x, y in neo_trellis.pressed_keys)

    # Handle newly pressed buttons
    for button in current_pressed - pressed_buttons:
        x, y = button_mappings[button]
        neo_trellis.pixels[x, y] = (255, 255, 255)  # Bright white
        gamepad.press_buttons(button)

    # Handle released buttons
    for button in pressed_buttons - current_pressed:
        x, y = button_mappings[button]
        neo_trellis.pixels[x, y] = button_colors[button]  # Return to original color
        gamepad.release_buttons(button)

    pressed_buttons = current_pressed
    time.sleep(0.01)
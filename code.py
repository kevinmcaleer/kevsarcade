import usb_hid
from adafruit_hid.mouse import Mouse
from analogio import AnalogIn
import digitalio
import board
import time

# Set up HID mouse
mouse = Mouse(usb_hid.devices)

# Analog joystick inputs
x_axis = AnalogIn(board.A0)
y_axis = AnalogIn(board.A1)

# Arcade buttons
button_1 = digitalio.DigitalInOut(board.GP0)
button_1.switch_to_input(pull=digitalio.Pull.UP)
button_2 = digitalio.DigitalInOut(board.GP1)
button_2.switch_to_input(pull=digitalio.Pull.UP)

# Function to scale analog values (from 0-65535) to a smaller range
def scale_axis(value):
    return int((value - 32768) / 500)  # Adjust divisor for sensitivity

while True:
    # Read and scale joystick values
    x_val = scale_axis(x_axis.value)
    y_val = scale_axis(y_axis.value)

    # Move the mouse based on joystick position
    mouse.move(x=x_val, y=y_val)

    # Button presses can emulate left and right clicks
    if not button_1.value:
        mouse.click(Mouse.LEFT_BUTTON)
    if not button_2.value:
        mouse.click(Mouse.RIGHT_BUTTON)

    time.sleep(0.1)

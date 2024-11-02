# A simple joystick controller using CircuitPython and Adafruit HID library.

import board
import analogio
import digitalio
import usb_hid
from adafruit_hid.gamepad import Gamepad

# Set up joystick potentiometers as analog inputs
x_axis = analogio.AnalogIn(board.A0)  # Connect VRX
y_axis = analogio.AnalogIn(board.A1)  # Connect VRY

# Set up joystick button
joystick_button = digitalio.DigitalInOut(board.D3)
joystick_button.switch_to_input(pull=digitalio.Pull.UP)

# Set up arcade buttons
button_1 = digitalio.DigitalInOut(board.D4)
button_1.switch_to_input(pull=digitalio.Pull.UP)

button_2 = digitalio.DigitalInOut(board.D5)
button_2.switch_to_input(pull=digitalio.Pull.UP)

# Initialize gamepad
gamepad = Gamepad(usb_hid.devices)

# Function to scale analog values (from 0-65535 to -127 to 127)
def scale_axis(value):
    return int((value - 32768) / 256)

while True:
    # Read and scale joystick values
    x_val = scale_axis(x_axis.value)
    y_val = scale_axis(y_axis.value)
    
    # Joystick button
    joystick_btn_pressed = not joystick_button.value
    
    # Arcade buttons
    btn1_pressed = not button_1.value
    btn2_pressed = not button_2.value
    
    # Send joystick report
    gamepad.move_joystick(x_val, y_val, joystick_btn_pressed, btn1_pressed, btn2_pressed)

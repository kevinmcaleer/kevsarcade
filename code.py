import usb_hid
from adafruit_hid.mouse import Mouse
from analogio import AnalogIn
import digitalio
import board
import time
from hid_gamepad import Gamepad

gamepad = Gamepad(devices=usb_hid.devices)

# Set up HID mouse
# mouse = Mouse(usb_hid.devices)

# Analog joystick inputs
x_axis = AnalogIn(board.A0)
y_axis = AnalogIn(board.A1)

# Arcade buttons
# button_1 = digitalio.DigitalInOut(board.GP0)
# button_1.switch_to_input(pull=digitalio.Pull.UP)
# button_2 = digitalio.DigitalInOut(board.GP1)
# button_2.switch_to_input(pull=digitalio.Pull.UP)
# button_3 = digitalio.DigitalInOut(board.GP2)
# button_3.switch_to_input(pull=digitalio.Pull.UP)

button_pins = (board.GP0, board.GP1, board.GP2)
gamepad_buttons = (1, 2, 3)

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP


# Function to scale analog values (from 0-65535) to a smaller range
def scale_axis(value):
    return int((value - 32768) / 500)  # Adjust divisor for sensitivity

# Equivalent of Arduino's map() function.
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min



while True:
    # Read and scale joystick values
#     x_val = scale_axis(x_axis.value)
#     y_val = scale_axis(y_axis.value)

    # Move the gamepad based on joystick position
#     gamepad.move_joysticks(x=x_val, y=y_val)

    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if button.value:
            gamepad.release_buttons(gamepad_button_num)
            print(" release", gamepad_button_num, end="")
        else:
            gamepad.press_buttons(gamepad_button_num)
            print(" press", gamepad_button_num, end="")

    # Convert range[0, 65535] to -127 to 127
    gamepad.move_joysticks(
        x=range_map(x_axis.value, 0, 65535, -127, 127),
        y=range_map(y_axis.value, 0, 65535, -127, 127),
    )
    print(" x", x_axis.value, "y", y_axis.value)
    time.sleep(0.1)

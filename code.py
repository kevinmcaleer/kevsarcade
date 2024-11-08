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

CENTER_X = 53000
CENTER_Y = 53000
DEADZONE = 1800 # Deadzone around the center for stability

# Initialize previous values for filtering
prev_x = 0
prev_y = 0
ALPHA = 0.7  # Smoothing factor, closer to 1 is smoother but more lagged

button_pins = (board.GP0, board.GP1, board.GP2)
gamepad_buttons = (1, 2, 3)

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP


# Function to scale analog values (from 0-65535) to a smaller range
def scale_axis(value, center):
    if abs(value - center) < DEADZONE:
        return 0 # stay at zero within dead zone
    elif value < center:
        # Map lower half to -127
        return int(((value - center) / (center - 0)) * 127)
    else:
        # Map upper half to +127
        return int(((value - center) / (65535 - center)) * 127)  

# Equivalent of Arduino's map() function.
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min



while True:
    # Read and scale values, adjusting for deadzone and center
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if button.value:
            gamepad.release_buttons(gamepad_button_num)
            print(" release", gamepad_button_num, end="")
        else:
            gamepad.press_buttons(gamepad_button_num)
            print(" press", gamepad_button_num, end="")

    # Convert range[0, 65535] to -127 to 127
    x = scale_axis(x_axis.value, CENTER_X)
    y = scale_axis(y_axis.value, CENTER_Y)
    
    # Apply filtering
    filtered_x = int(ALPHA * prev_x + (1 - ALPHA) * x)
    filtered_y = int(ALPHA * prev_y + (1 - ALPHA) * y)
    
    prev_x = filtered_x
    prev_y = filtered_y
    
    gamepad.move_joysticks(
        x = filtered_x,
        y = filtered_y,
    )
    print(" x", filtered_x, "y", filtered_y)
    time.sleep(0.01)

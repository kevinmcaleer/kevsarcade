import usb_hid

# Enable only keyboard and mouse for HID
usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE))

# config.py
# Connection settings for the RoArm.

ARM_HOST = "192.168.4.1"   # used only when ARM_USE_SERIAL is False (Wi-Fi)

ARM_USE_SERIAL = True      # True  -> USB-C cable via SERIAL_PORT
                           # False -> Wi-Fi via ARM_HOST
SERIAL_PORT = "COM3"       # arm's port
SERIAL_BAUD = 115200       # check your arm's firmware docs for the exact rate
# import requests
# import json
# import time

# ARM_IP = "192.168.4.1"

# def send(command):
#     url = f"http://{ARM_IP}/js?json={json.dumps(command)}"
#     return requests.get(url, timeout=5).text

# # 1. Return to the initial position
# send({"T": 100})
# time.sleep(5)

# # 2. Rotate the base 30 degrees to the left (slowly)
# send({"T": 121, "joint": 1, "angle": 30, "spd": 0, "acc": 0})
# time.sleep(1)

# # 3. Rotate the base 30 degrees to the right
# send({"T": 121, "joint": 4, "angle": -30, "spd": 0, "acc": 0})
# time.sleep(1)

# # 6. Read the arm position
# print(send({"T": 105}))

import json
import time

import serial  # pip install pyserial

PORT = "COM3"   # TODO: change to your arm's port (Device Manager -> Ports (COM & LPT))
BAUD = 115200   # RoArm-M3 serial speed


def open_arm(port=PORT, baud=BAUD):
    """Open the USB-C serial connection to the arm."""
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baud
    ser.timeout = 1
    # Keep DTR/RTS low BEFORE opening, otherwise opening the port can
    # reset the arm's controller board.
    ser.dtr = False
    ser.rts = False
    ser.open()
    return ser


def send(ser, command):
    """Send one JSON command. Over serial each command is one line ending in a newline."""
    line = json.dumps(command, separators=(",", ":")) + "\n"
    ser.write(line.encode("utf-8"))


def read_json(ser, expected_t, timeout=2.0):
    """Read lines until a JSON message with "T" == expected_t arrives (or timeout).

    The arm may also print other lines, so anything that is not the
    message we want is skipped.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        raw = ser.readline().decode("utf-8", errors="ignore").strip()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if data.get("T") == expected_t:
            return data
    return None


def main():
    ser = open_arm()
    try:
        time.sleep(2)  # give the board a moment after the port opens

        # 1. Return to the initial position
        send(ser, {"T": 100})
        time.sleep(5)

        # 2. Rotate the base 30 degrees to the left
        send(ser, {"T": 121, "joint": 2, "angle": 30, "spd": 10, "acc": 10})
        time.sleep(2)

        # 3. Rotate the base 30 degrees to the right
        send(ser, {"T": 121, "joint": 3, "angle": -30, "spd": 10, "acc": 10})
        time.sleep(2)

        # 6. Read the arm position (the reply to T:105 has "T": 1051)
        ser.reset_input_buffer()
        send(ser, {"T": 105})
        print(read_json(ser, expected_t=1051))
    finally:
        ser.close()  # always release the port, even if something failed


if __name__ == "__main__":
    main()
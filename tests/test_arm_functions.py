# # import requests
# # import json
# # import time

# # ARM_IP = "192.168.4.1"

# # def send(command):
# #     url = f"http://{ARM_IP}/js?json={json.dumps(command)}"
# #     return requests.get(url, timeout=5).text

# # # 1. Return to the initial position
# # send({"T": 100})
# # time.sleep(5)

# # # 2. Rotate the base 30 degrees to the left (slowly)
# # send({"T": 121, "joint": 1, "angle": 30, "spd": 0, "acc": 0})
# # time.sleep(1)

# # # 3. Rotate the base 30 degrees to the right
# # send({"T": 121, "joint": 4, "angle": -30, "spd": 0, "acc": 0})
# # time.sleep(1)

# # # 6. Read the arm position
# # print(send({"T": 105}))

# import json
# import time

# import serial  # pip install pyserial

# PORT = "COM3"   # TODO: change to your arm's port (Device Manager -> Ports (COM & LPT))
# BAUD = 115200   # RoArm-M3 serial speed


# def open_arm(port=PORT, baud=BAUD):
#     """Open the USB-C serial connection to the arm."""
#     ser = serial.Serial()
#     ser.port = port
#     ser.baudrate = baud
#     ser.timeout = 1
#     # Keep DTR/RTS low BEFORE opening, otherwise opening the port can
#     # reset the arm's controller board.
#     ser.dtr = False
#     ser.rts = False
#     ser.open()
#     return ser


# def send(ser, command):
#     """Send one JSON command. Over serial each command is one line ending in a newline."""
#     line = json.dumps(command, separators=(",", ":")) + "\n"
#     ser.write(line.encode("utf-8"))


# def read_json(ser, expected_t, timeout=2.0):
#     """Read lines until a JSON message with "T" == expected_t arrives (or timeout).

#     The arm may also print other lines, so anything that is not the
#     message we want is skipped.
#     """
#     deadline = time.time() + timeout
#     while time.time() < deadline:
#         raw = ser.readline().decode("utf-8", errors="ignore").strip()
#         if not raw:
#             continue
#         try:
#             data = json.loads(raw)
#         except json.JSONDecodeError:
#             continue
#         if data.get("T") == expected_t:
#             return data
#     return None


# def main():
#     ser = open_arm()
#     try:
#         time.sleep(2)  # give the board a moment after the port opens

#         # 1. Return to the initial position
#         send(ser, {"T": 100})
#         time.sleep(5)

#         # 2. Rotate the base 30 degrees to the left
#         send(ser, {"T": 121, "joint": 2, "angle": 30, "spd": 10, "acc": 10})
#         time.sleep(2)

#         # 3. Rotate the base 30 degrees to the right
#         send(ser, {"T": 121, "joint": 3, "angle": -30, "spd": 10, "acc": 10})
#         time.sleep(2)

#         # 6. Read the arm position (the reply to T:105 has "T": 1051)
#         ser.reset_input_buffer()
#         send(ser, {"T": 105})
#         print(read_json(ser, expected_t=1051))
#     finally:
#         ser.close()  # always release the port, even if something failed


# if __name__ == "__main__":
#     main()



"""Rock-paper-scissors gesture test for the RoArm-M3 Pro over USB-C serial.

Run from the project root with the venv active:

    python tools/arm_gestures.py demo --dry-run          # only prints commands, no arm needed
    python tools/arm_gestures.py calibrate --port COM3   # find the gripper angles (do this first)
    python tools/arm_gestures.py demo --port COM3        # play the three gestures

The Arm class has the same methods as the project's ArmInterface
(ready, pump, show, stop), so it can become the base of RoArmController.
"""
import argparse
import json
import math
import time

PORT = "COM3"
BAUD = 115200

# --- Motion settings (keep these gentle) -----------------------------------
SPEED = 10             # NOTE: 0 may mean "maximum speed" on this arm, so never use 0
ACC = 10
STEP_TIME = 0.7        # seconds to wait after each joint move

GRIPPER_JOINT = 6
PUMP_JOINT = 4         # wrist pitch: the "fist pump"
ROLL_JOINT = 5         # wrist roll: the scissors wiggle
PUMP_DELTA_DEG = 15    # how far the pump moves away from the ready pose
PUMPS = 3
WIGGLE_DEG = 15
WIGGLES = 3

# --- Gripper angles in degrees: FILL THESE IN using the calibrate mode ------
GRIPPER_ANGLES = {
    "rock": 254.8,       # gripper fully closed
    "paper": 171.3,      # gripper fully open
    "scissors": 232.2,   # gripper half open
}
MAX_CALIBRATION_STEP_DEG = 10

FAKE_FEEDBACK = {"T": 1051, "b": 0.0, "s": 0.0, "e": 1.57, "t": 0.0, "r": 0.0, "g": 3.14}


class Arm:
    def __init__(self, port=PORT, dry_run=False):
        self.dry_run = dry_run
        self.ser = None
        self.ready_deg = {}
        if not dry_run:
            import serial  # pip install pyserial

            ser = serial.Serial()
            ser.port = port
            ser.baudrate = BAUD
            ser.timeout = 1
            ser.dtr = False   # set before open() so opening the port does not reset the board
            ser.rts = False
            ser.open()
            self.ser = ser
            time.sleep(2)

    # ---- low level ----
    def _send(self, command):
        line = json.dumps(command, separators=(",", ":"))
        if self.dry_run:
            print("  >>", line)
            return
        self.ser.write((line + "\n").encode("utf-8"))

    def _feedback(self, timeout=2.0):
        if self.dry_run:
            return dict(FAKE_FEEDBACK)
        self.ser.reset_input_buffer()
        self._send({"T": 105})
        deadline = time.time() + timeout
        while time.time() < deadline:
            raw = self.ser.readline().decode("utf-8", errors="ignore").strip()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if data.get("T") == 1051:
                return data
        return None

    def joint_deg(self):
        """Current joint angles in degrees, read from the arm (feedback is in radians)."""
        fb = self._feedback()
        if fb is None:
            raise RuntimeError("No feedback from the arm. Check the port and the power supply.")
        keys = {1: "b", 2: "s", 3: "e", 4: "t", 5: "r", 6: "g"}
        return {joint: math.degrees(fb[key]) for joint, key in keys.items()}

    def move_joint(self, joint, angle_deg):
        self._send({"T": 121, "joint": joint, "angle": round(angle_deg, 1),
                    "spd": SPEED, "acc": ACC})
        if not self.dry_run:
            time.sleep(STEP_TIME)

    # ---- the interface the game engine needs ----
    def ready(self):
        self._send({"T": 100})            # initial position
        if not self.dry_run:
            time.sleep(5)
        self.ready_deg = self.joint_deg()  # remember the ready pose

    def pump(self):
        base = self.ready_deg[PUMP_JOINT]
        for _ in range(PUMPS):
            self.move_joint(PUMP_JOINT, base + PUMP_DELTA_DEG)
            self.move_joint(PUMP_JOINT, base)

    def show(self, move):
        angle = GRIPPER_ANGLES[move]
        if angle is None:
            if not self.dry_run:
                raise RuntimeError("Gripper angles are not calibrated. Run the calibrate mode first.")
            angle = 0.0                    # placeholder, dry run only
        self.move_joint(GRIPPER_JOINT, angle)
        if move == "scissors":
            roll = self.ready_deg[ROLL_JOINT]
            for _ in range(WIGGLES):
                self.move_joint(ROLL_JOINT, roll + WIGGLE_DEG)
                self.move_joint(ROLL_JOINT, roll - WIGGLE_DEG)
            self.move_joint(ROLL_JOINT, roll)

    def stop(self):
        """Torque off. WARNING: the arm will go limp and may drop. Emergency use only."""
        self._send({"T": 210, "cmd": 0})

    def close(self):
        if self.ser:
            self.ser.close()


def calibrate(arm):
    arm.ready()
    print("Move the gripper in small steps. Type +5 or -5 (max "
          f"{MAX_CALIBRATION_STEP_DEG}), or q to quit.")
    print("Write down the angle for: fully closed, fully open, half open.")
    print("Stop BEFORE the gripper strains against its end stop.")
    while True:
        current = arm.joint_deg()[GRIPPER_JOINT]
        text = input(f"gripper at {current:.1f} deg > ").strip().lower()
        if text == "q":
            return
        try:
            step = float(text)
        except ValueError:
            continue
        step = max(-MAX_CALIBRATION_STEP_DEG, min(MAX_CALIBRATION_STEP_DEG, step))
        arm.move_joint(GRIPPER_JOINT, current + step)


def demo(arm):
    for move in ("rock", "paper", "scissors"):
        print(f"--- {move} ---")
        arm.ready()
        arm.pump()
        arm.show(move)
        time.sleep(0 if arm.dry_run else 1.5)
    arm.ready()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["demo", "calibrate"])
    parser.add_argument("--port", default=PORT)
    parser.add_argument("--dry-run", action="store_true",
                        help="print the commands instead of sending them")
    args = parser.parse_args()

    arm = Arm(args.port, dry_run=args.dry_run)
    try:
        (calibrate if args.mode == "calibrate" else demo)(arm)
    finally:
        arm.close()


if __name__ == "__main__":
    main()
import requests
import json
import time

ARM_IP = "192.168.4.1"

PUMP_JOINT = 4        # wrist pitch joint
PUMP_DELTA_DEG = 15   # how far it moves away from ready pose
PUMPS = 3
SPEED = 40
ACC = 10

GRIPPER_JOINT = 6
ROLL_JOINT = 5
WIGGLE_DEG = 30
WIGGLES = 3
ELBOW_JOINT = 3   # elbow


GRIPPER_ANGLES = {
    "rock": 254.8,       # gripper fully closed
    "paper": 171.3,      # gripper fully open
    "scissors": 232.2,   # gripper half open
}

def send(command):
    url = f"http://{ARM_IP}/js?json={json.dumps(command)}"
    return requests.get(url, timeout=5).text


def ready():
    """Send the arm back to its initial position."""
    try:
        send({"T": 100})
        time.sleep(1)
        return True
    except Exception as e:
        print(f"ready() failed: {e}")
        return False



def pump():
    """Perform the 3-pump countdown motion."""
    try:
        for _ in range(PUMPS):
            # Both joints move down together
            send({"T": 121, "joint": PUMP_JOINT, "angle": 30,
                  "spd": SPEED, "acc": ACC})
            send({"T": 121, "joint": ELBOW_JOINT, "angle": 20,
                  "spd": SPEED, "acc": ACC})
            time.sleep(0.4)

            # Both joints move back up together
            send({"T": 121, "joint": PUMP_JOINT, "angle": 0,
                  "spd": SPEED, "acc": ACC})
            send({"T": 121, "joint": ELBOW_JOINT, "angle": 90,
                  "spd": SPEED, "acc": ACC})
            time.sleep(0.4)
        return True
    except Exception as e:
        print(f"pump() failed: {e}")
        return False


    
def show(move):
    """Move the gripper to display the chosen gesture."""
    try:
        angle = GRIPPER_ANGLES[move]
        send({"T": 121, "joint": GRIPPER_JOINT, "angle": angle,
              "spd": SPEED, "acc": ACC})
        time.sleep(0.5)

        if move == "scissors":
            send({"T": 121, "joint": ROLL_JOINT, "angle": -WIGGLE_DEG,
                    "spd": SPEED, "acc": ACC})
            time.sleep(0.3)
               

        return True
    except Exception as e:
        print(f"show() failed: {e}")
        return False

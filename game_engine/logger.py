import csv
import os
from datetime import datetime


class RoundLogger:
    COLUMNS = ["timestamp", "round", "mode", "player_move", "arm_move",
               "result", "commit_time", "capture_time", "latency_s"]

    def __init__(self, path):
        self.path = path
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)       # create logs if missing
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(self.COLUMNS)  # header row, written once

    def log_round(self, round_no, mode, player_move, arm_move, result,
                  commit_time, capture_time, latency_s):
        row = [datetime.now().isoformat(timespec="seconds"), round_no, mode,
               player_move, arm_move, result,
               round(commit_time, 3), round(capture_time, 3), round(latency_s, 3)]
        with open(self.path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)
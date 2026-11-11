import time

import config
from game_engine.rules import decide_winner
from game_engine.states import GameState

S = GameState

# Which state is allowed follow which (ERROR is handled by _fail)
ALLOWED = {
    S.IDLE:      {S.READY},
    S.READY:     {S.COMMIT, S.IDLE},
    S.COMMIT:    {S.COUNTDOWN},
    S.COUNTDOWN: {S.CAPTURE},
    S.CAPTURE:   {S.REVEAL, S.RETRY, S.READY},   # READY = round voided
    S.RETRY:     {S.COUNTDOWN},
    S.REVEAL:    {S.RESULT},
    S.RESULT:    {S.READY, S.GAME_OVER},
    S.GAME_OVER: {S.IDLE},
    S.ERROR:     {S.IDLE},
}


class GameEngine:
    def __init__(self, arm, vision, picker, scoreboard, logger=None):
        self.arm = arm
        self.vision = vision
        self.picker = picker
        self.scoreboard = scoreboard
        self.logger = logger

        self.state = S.IDLE
        self.history = []             #player's moves, oldest first
        self.round_number = 0
        self._committed_move = None   #private: hidden until the reveal
        self.last_player_move = None
        self.last_arm_move = None     #filled only AFTER the reveal
        self.last_result = None
        self.error = None

    #public API
    def start_game(self):
        self.scoreboard.reset()
        self.history.clear()
        self.round_number = 0
        self._committed_move = None
        self.last_player_move = None
        self.last_arm_move = None
        self.last_result = None
        self.error = None
        self.state = S.IDLE            #allow restarting from any state (smart)
        self.arm.ready()
        self._set_state(S.READY)

    def play_round(self):
        if self.state != S.READY:
            raise RuntimeError(f"Cannot play a round in state {self.state.name}")
        try:
            self._play_round()
        except Exception as exc:       #device failure, illegal stuff...
            self._fail(f"{type(exc).__name__}: {exc}")

    def reset(self):
        self._committed_move = None
        self.error = None
        self.state = S.IDLE

    def get_status(self):
        return {
            "state": self.state.name,
            "round": self.round_number,
            "player_score": self.scoreboard.player_score,
            "arm_score": self.scoreboard.arm_score,
            "draws": self.scoreboard.draws,
            "last_player_move": self.last_player_move,
            "last_arm_move": self.last_arm_move,   #never the committed move!!
            "last_result": self.last_result,
            "match_winner": self.scoreboard.match_winner(),
            "error": self.error,
        }

    #internals
    def _set_state(self, new_state):
        if new_state not in ALLOWED[self.state]:
            raise RuntimeError(f"Illegal transition {self.state.name} -> {new_state.name}")
        self.state = new_state

    def _fail(self, message):
        self.error = message
        self._committed_move = None
        self.state = S.ERROR
        try:
            self.arm.stop()
        except Exception:
            pass                       #there is nothing we can do...

    def _play_round(self):
        self.round_number += 1
        self.last_player_move = None
        self.last_arm_move = None
        self.last_result = None
        self.error = None

        # 1.COMMIT:the arm decides BEFORE the camera is ever read
        self._set_state(S.COMMIT)
        self._committed_move = self.picker.choose_move(self.history)
        commit_time = time.time()

        # 2-3.COUNTDOWN + CAPTURE, with retries if no gesture is found
        player_move = None
        for attempt in range(config.MAX_RETRIES + 1):
            if attempt > 0:
                self._set_state(S.RETRY)
            self._set_state(S.COUNTDOWN)
            self.arm.pump()
            countdown_end = time.time()
            self._set_state(S.CAPTURE)
            capture_time = time.time()
            player_move = self.vision.read_gesture()
            if player_move is not None:
                break

        if player_move is None:        # round voided, nothing is scored
            self._committed_move = None
            self.round_number -= 1
            self.error = "No gesture detected, round cancelled"
            self.arm.ready()
            self._set_state(S.READY)
            return

        # 4. REVEAL
        self._set_state(S.REVEAL)
        self.arm.show(self._committed_move)
        latency = time.time() - countdown_end
        self.last_arm_move = self._committed_move   # now it may be shown

        # 5. RESULT
        self._set_state(S.RESULT)
        result = decide_winner(player_move, self._committed_move)
        self.scoreboard.record(result)
        self.history.append(player_move)
        self.last_player_move = player_move
        self.last_result = result
        if self.logger:
            self.logger.log_round(self.round_number, type(self.picker).__name__,
                                  player_move, self._committed_move, result,
                                  commit_time, capture_time, latency)
        self._committed_move = None

        # 6. next
        if self.scoreboard.match_winner() is not None:
            self._set_state(S.GAME_OVER)
        else:
            self.arm.ready()
            self._set_state(S.READY)
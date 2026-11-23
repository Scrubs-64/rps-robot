#### Nov. 20th, week 1 - 2
**Week 1:**
A project scope has been settled on. We will use Mediapipe to perform the gesture recognition task, Pyside6 for the dashboard UI, the Ro-Arm 3 Pro to play machine moves.

- **File structure:**
├── README.md              setup steps, who owns what, team agreements to fill in
├── requirements.txt       team dependencies
├── requirements-dev.txt   same plus pytest
├── pytest.ini             makes `python -m pytest` work from the root
├── .gitignore
├── config.py              shared settings (rounds to win, camera index, arm IP...)
├── main.py                wires everything together; `python main.py --mock`
├── common/                THE CONTRACT (changed only by team agreement)
│   ├── moves.py           "rock"/"paper"/"scissors", BEATS, counter_to()
│   └── interfaces.py      what the arm and vision modules must provide
├── game_engine/           Member 3:
│   ├── states.py, rules.py, scoreboard.py, engine.py, logger.py
│   └── pickers/           base.py, random_picker.py, make_picker()
├── arm_controller/        Member 1: MockArm (working) + RoArmController (stub)
├── vision/                Member 2: ScriptedVision and KeyboardVision (working) + VisionModule (stub)
├── ui/                    Member 4: dashboard stub
├── tools/                 keyboard_game.py (the Week 3 no-CV game)
├── tests/                 rules, moves, fakes, a skipped fairness test
├── docs/                  interfaces.md, git_workflow.md, game_design.md
├── logs/  data/

We found out that the mediapipe model already performs most if not all of our machine learning efficiently. The program can recognize rock, paper and scissor (fist, open-palm, and victory-sign classes). However, it must be from the "front" of your hand. Hence we need to place the camera kind of laying on the table facing up instead of being on the arm itself.
To test out the capabilities of the model, a test game has been written, one for player vs player, the other for player vs computer generated move. The model can detect hand gesture extremely fast and accurately.

We have also successfully started controlling the Ro-Arm. The arm is able to perform many movements in relatively fast speed.

**Week 2:**
Game engine is being developed. 

Because of our faster than expected progress, we are thinking of new directions to push our project in. As an effort to humanize the Ro-Arm, we want to implement a feature / game rule where the arm follows the player's arm movements during the countdown to committing to a move, as two people do in an actual game of rock paper scissors. Using the coordinates of the wrist on screen, it is easy to detect the "pumping" movement of the player. However, this cannot be achieved with a webcam laying on the table, so we have decided to eventually mount the webcam horizontally looking at the player's hand.
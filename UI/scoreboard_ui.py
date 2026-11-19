from pathlib import Path
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap

class ScoreboardUI:

    def __init__(self):
        self.ui_dir = Path(__file__).resolve().parent / "scoreboard_ui.ui"
        loader = QUiLoader()
        self.window = loader.load(str(self.ui_dir))

        self.window.rock.setPixmap(QPixmap(str(self.ui_dir / "rock.jpg")))
        self.window.paper.setPixmap(QPixmap(str(self.ui_dir / "paper.png")))
        self.window.scissor.setPixmap(QPixmap(str(self.ui_dir / "scissor.jpg")))
        self.rule = ['BO10 Regular\nR.P.S.', 'BO3 Regular\nR.P.S.'] 
        # ^^ just a place holder, we can put in any other rules we come up with --Faye


    def show(self):
        self.window.show()

    def setPlayerScore(self, score):
        self.window.playerScore.setText(str(score))

    def setCompScore(self, score):
            self.window.computerScore.setText(str(score))

    def setGameRule(self, mode):
         self.window.comgameRuleputerScore.setText(self.rule[mode])
         


if __name__ == "__main__":
    app = QApplication([])

    gui = ScoreboardUI()
    gui.show()

    app.exec()
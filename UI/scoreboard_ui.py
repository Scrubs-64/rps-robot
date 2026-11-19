from pathlib import Path
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap

class ScoreboardUI:
    def __init__(self):
        self.ui_dir = Path(__file__).resolve().parent
        loader = QUiLoader()
        self.window = loader.load(
            str(self.ui_dir / "scoreboard_ui.ui")
        )
        self.window.rock.setPixmap(
            QPixmap(str(self.ui_dir / "rock.jpg"))
        )
        self.window.paper.setPixmap(
            QPixmap(str(self.ui_dir / "paper.png"))
        )
        self.window.scissor.setPixmap(
            QPixmap(str(self.ui_dir / "scissor.jpg"))
        )

    def show(self):
        self.window.show()


if __name__ == "__main__":
    app = QApplication([])

    gui = ScoreboardUI()
    gui.show()

    app.exec()
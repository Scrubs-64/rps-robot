from pathlib import Path
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
import sys

from PySide6 import QtWidgets
from PySide6 import QtGui, QtCore
from PySide6.QtCore import * 
from PySide6.QtGui import *
from PySide6.QtWidgets import QFileDialog, QMainWindow, QMessageBox

import cv2
import numpy as np # cv2 mat is wrapped by numpy

class ScoreboardUI:

    def __init__(self):
        self.ui_dir = Path(__file__).resolve().parent
        loader = QUiLoader()
        self.window = loader.load(str(self.ui_dir / "scoreboard_ui.ui"))
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.cap = cv2.VideoCapture(0) # Open default camera
        self.timer.start(30)

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

    def display_video_stream(self):
        ret, frame = self.cap.read() # Get status and frame
        if ret:
            self.display(frame) 

    def display(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0], 
                        frame.strides[0], QImage.Format_RGB888)
        
        self.window.cameraFeed.setPixmap(QPixmap.fromImage(image))
         


if __name__ == "__main__":
    app = QApplication([])

    gui = ScoreboardUI()
    gui.show()

    app.exec()
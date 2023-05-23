import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
from functions import get_text_from_database, play_text_with_tts, get_story_titles_from_database

class BedStorysGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.media_player = None

    def initUI(self):
        self.setStyleSheet("background-color: #EFEFEF;")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.setFont(font)
        self.setWindowTitle("Mat´s Geschichten Vorleser")

        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(50, 50, 200, 400)
        self.listWidget.setStyleSheet("background-color: #D3D3D3; border: 2px solid black;")
        self.listWidget.setFont(QtGui.QFont("Arial", 14))
        self.listWidget.itemClicked.connect(self.play_text_from_title)

        titles = self.get_titles_from_database()
        for title in titles:
            item = QtWidgets.QListWidgetItem(title)
            item.setBackground(QtGui.QColor("#F5F5F5"))
            self.listWidget.addItem(item)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(270, 50, 400, 400)
        self.textEdit.setStyleSheet("background-color: #D3D3D3; border: 2px solid black;")
        self.textEdit.setFont(QtGui.QFont("Arial", 14))
        self.textEdit.setReadOnly(True)

        self.playButton = QtWidgets.QPushButton("Play", self)
        self.playButton.setGeometry(50, 470, 80, 40)
        self.playButton.setStyleSheet("background-color: green; color: white; border-radius: 5px;")
        self.playButton.clicked.connect(self.play_current_text)

        self.pauseButton = QtWidgets.QPushButton("Pause", self)
        self.pauseButton.setGeometry(150, 470, 80, 40)
        self.pauseButton.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
        self.pauseButton.clicked.connect(self.pause_audio)

        self.resumeButton = QtWidgets.QPushButton("Resume", self)
        self.resumeButton.setGeometry(250, 470, 80, 40)
        self.resumeButton.setStyleSheet("background-color: blue; color: white; border-radius: 5px;")
        self.resumeButton.clicked.connect(self.resume_audio)

        self.volumeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeSlider.setGeometry(350, 470, 200, 40)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(self.set_volume)

        self.setGeometry(500, 300, 700, 550)
        self.show()

    def get_titles_from_database(self):
        titles = get_story_titles_from_database()
        return titles

    def play_text_from_title(self, item):
        text = get_text_from_database(item.text())
        if text:
            self.current_text = text
            self.textEdit.setText(text)
            self.playButton.setEnabled(True)

    def play_current_text(self):
        self.playButton.setEnabled(False)
        file_name = play_text_with_tts(self.current_text)

        if self.media_player is not None:
            self.media_player.stop()

        self.media_player = QtMultimedia.QMediaPlayer(self)
        self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file_name)))
        self.media_player.play()

    def pause_audio(self):
        if self.media_player is not None:
            self.media_player.pause()

    def resume_audio(self):
        if self.media_player is not None:
            self.media_player.play()

    def set_volume(self, value):
        if self.media_player is not None:
            self.media_player.setVolume(value)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = BedStorysGUI()
    sys.exit(app.exec_())


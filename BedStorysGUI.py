import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
from functions import get_text_from_database, play_text_with_tts, get_story_titles_from_database

class BedStorysGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.move(50, 50)
        self.listWidget.resize(200, 400)
        self.listWidget.itemClicked.connect(self.play_text_from_title)

        titles = self.get_titles_from_database()
        for title in titles:
            self.listWidget.addItem(title)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.move(270, 50)
        self.textEdit.resize(400, 400)
        self.textEdit.setReadOnly(True)

        self.playButton = QtWidgets.QPushButton("Play", self)
        self.playButton.move(50, 470)

        self.playButton.clicked.connect(self.play_current_text)

        self.setGeometry(500, 300, 700, 550)
        self.setWindowTitle("Mat´s Geschichten Vorleser")
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

        self.media_player = QtMultimedia.QMediaPlayer(self)
        self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file_name)))
        self.media_player.play()

        while self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            QtWidgets.QApplication.processEvents()

        self.playButton.setEnabled(True)

# Hauptprogramm
if __name__ == '__main__':
    # Erstelle eine Qt-Anwendung
    app = QtWidgets.QApplication(sys.argv)
    # Erstelle ein BedStorysGUI-Objekt
    ex = BedStorysGUI()
    # Starte die Anwendung und beende sie, wenn sie beendet wird
    sys.exit(app.exec_())

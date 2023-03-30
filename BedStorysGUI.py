import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
from functions import get_text_from_database, play_text_with_tts, get_story_titles_from_database

class BedStorysGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.media_player = None  # Fügt das Attribut media_player hinzu und initialisiert es mit None

    def initUI(self):
        # Ändert die Hintergrundfarbe des Fensters
        self.setStyleSheet("background-color: #EFEFEF;")
        
        # Ändert die Schriftart und -größe des Fenstertitels
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.setFont(font)
        self.setWindowTitle("Mat´s Geschichten Vorleser")
        
        # Erstellen des ListWidget
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(50, 50, 200, 400)
        self.listWidget.setStyleSheet("background-color: #D3D3D3; border: 2px solid black;")
        self.listWidget.setFont(QtGui.QFont("Arial", 14))
        self.listWidget.itemClicked.connect(self.play_text_from_title)

        # Füge die Titel Elemente der Liste hinzu
        titles = self.get_titles_from_database()
        for title in titles:
            item = QtWidgets.QListWidgetItem(title)
            item.setBackground(QtGui.QColor("#F5F5F5"))
            self.listWidget.addItem(item)

        # Erstellenung des QTextEdit-Feld
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(270, 50, 400, 400)
        self.textEdit.setStyleSheet("background-color: #D3D3D3; border: 2px solid black;")
        self.textEdit.setFont(QtGui.QFont("Arial", 14))
        self.textEdit.setReadOnly(True)

        # Erstellenung der Buttons
        self.playButton = QtWidgets.QPushButton("Play", self)
        self.playButton.setGeometry(50, 470, 80, 40)
        self.playButton.setStyleSheet("background-color: green; color: white; border-radius: 5px;")
        self.playButton.clicked.connect(self.play_current_text)

        self.pauseButton = QtWidgets.QPushButton('Pause', self)
        self.pauseButton.setGeometry(150, 470, 80, 40)
        self.pauseButton.setStyleSheet("background-color: red; color: white; border-radius: 5px;")
        self.pauseButton.clicked.connect(self.pause_audio)

        self.resumeButton = QtWidgets.QPushButton('Resume', self)
        self.resumeButton.setGeometry(250, 470, 80, 40)
        self.resumeButton.setStyleSheet("background-color: blue; color: white; border-radius: 5px;")
        self.resumeButton.clicked.connect(self.resume_audio)

        # Größe des Fensters festlegen
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

# Hauptprogramm
if __name__ == '__main__':
    # Erstelle eine Qt-Anwendung
    app = QtWidgets.QApplication(sys.argv)
    # Erstelle ein BedStorysGUI-Objekt
    ex = BedStorysGUI()
    # Starte die Anwendung und beende sie, wenn sie beendet wird
    sys.exit(app.exec_())
                                                                                                                                                                                                               
import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
from functions import get_text_from_database
from functions import play_text_with_tts
from functions import highlight_text_while_playing

# Die Hauptklasse für die GUI
class BedStorysGUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Ruft den Konstruktor der übergeordneten Klasse auf
        super().__init__()
        self.initUI()

    # Initialisiert die Benutzeroberfläche
    def initUI(self):
        # Erstelle einen Button
        btn = QtWidgets.QPushButton("Zufällige Geschichte", self)
        # Verbinde das Klicken des Buttons mit der Methode get_text
        btn.clicked.connect(self.get_text)
        #btn.resize(btn.sizeHint())
        btn.move(50, 50)

        # Erstelle eine TextEdit-Komponente
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.move(50, 100)
        self.textEdit.resize(400, 400)
        self.textEdit.setReadOnly(True)

        # Erstelle eine PushButton-Komponente
        # self.pauseButton = QtWidgets.QPushButton("Pause", self)
        # self.pauseButton.move(200, 50)

        # Verbinde das Klicken der Schaltfläche mit einer Methode
        # self.pauseButton.clicked.connect(self.pause_text)

        # Erstelle eine PushButton-Komponente
        # self.playButton = QtWidgets.QPushButton("Play", self)
        # self.playButton.move(300, 50)

        # Verbinde das Klicken der Schaltfläche mit einer Methode
        # self.playButton.clicked.connect(self.play_text)
        # self.playButton.setEnabled(False)

        # Setze das Fenster auf die gegebenen Koordinaten und Größe
        self.setGeometry(500, 300, 500, 550)
        # Setze den Fenstertitel
        self.setWindowTitle("Mat´s Geschichten Vorleser")
        # Zeige das Fenster
        self.show()

    # Holt einen zufälligen Text aus der Datenbank und setzt ihn im Label
    def get_text(self):
        text = get_text_from_database()
        if text:
            self.textEdit.setText(text)
            self.play_text(text)

    # Pausiert den Audio-Player
    def pause_text(self):
        self.media_player.pause()
        self.playButton.setEnabled(True)
        self.pauseButton.setEnabled(False)      

    # Spielt den gegebenen Text mit Text-to-Speech ab
    def play_text(self, text):
        file_name = play_text_with_tts(text)

        self.media_player = QtMultimedia.QMediaPlayer(self)
        self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file_name)))
        self.media_player.play()


# Hauptprogramm
if __name__ == '__main__':
    # Erstelle eine Qt-Anwendung
    app = QtWidgets.QApplication(sys.argv)
    # Erstelle ein BedStorysGUI-Objekt
    ex = BedStorysGUI()
    # Starte die Anwendung und beende sie, wenn sie beendet wird
    sys.exit(app.exec_())

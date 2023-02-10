from gtts import gTTS
import os
from PyQt5 import QtWidgets


def text_to_speech(text):
    tts = gTTS(text=text, lang='de')
    tts.save("output.mp3")
    os.system("start output.mp3")

class BedStorysGUI(QtWidgets.QMainWindow):
    # ...
    def play_text(self):
        text = self.get_text()
        if text:
            text_to_speech(text)

import sqlite3
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextEdit, QApplication
import os
from gtts import gTTS
import tempfile
import threading
import time

def text_to_speech(text):
    tts = gTTS(text=text, lang='de')
    tts.save("output.mp3")
    os.system("start output.mp3")

def get_text_from_database():
    conn = sqlite3.connect("bed_storys.db")
    c = conn.cursor()

    c.execute("SELECT text FROM Storys ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()
    conn.close()

    return result[0] if result else None

def play_text_with_tts(text):
    tts = gTTS(text=text, lang='de')

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        file_name = f.name
        tts.save(file_name)

    return file_name

def highlight_text_while_playing(text_edit, text, file_name):
    def play_audio():
        os.system(f'start {file_name}')

    def highlight_text():
        words = text.split()
        for i, word in enumerate(words):
            QApplication.processEvents()
            cursor = text_edit.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(word + ' ')
            cursor.setPosition(text_edit.toPlainText().index(word), QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor)
            text_edit.setTextCursor(cursor)
            time.sleep(0.5)
            
    play_thread = threading.Thread(target=play_audio)
    highlight_thread = threading.Thread(target=highlight_text)

    play_thread.start()
    highlight_thread.start()

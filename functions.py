import sqlite3
from PyQt5.QtWidgets import QTextEdit, QListWidget, QApplication
from PyQt5.QtGui import QTextCursor
import os
from gtts import gTTS
import tempfile
import threading

def text_to_speech(text):
    tts = gTTS(text=text, lang='de')
    tts.save("output.mp3")
    os.system("start output.mp3")

def get_story_titles_from_database():
    # Öffne die Datenbank
    conn = sqlite3.connect("bed_storys.db")
    c = conn.cursor()

    # Führe eine Abfrage aus, um alle Titel der Geschichten zu erhalten
    c.execute("SELECT name FROM Storys ORDER BY id ASC")
    rows = c.fetchall()

    # Schließe die Datenbank
    conn.close()

    # Extrahiere die Titel aus den Zeilen und gib sie als Liste zurück
    titles = [row[0] for row in rows]
    return titles


def get_text_from_database(title):
    conn = sqlite3.connect("bed_storys.db")
    c = conn.cursor()

    c.execute("SELECT text FROM Storys WHERE name=?", (title,))
    result = c.fetchone()
    conn.close()

    return result[0] if result else None

def play_text_with_tts(text):
    tts = gTTS(text=text, lang='de')

    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        file_name = f.name
        tts.save(file_name)

    return file_name

def play_story(title, text_edit):
    text = get_text_from_database(title)
    file_name = play_text_with_tts(text)
    play_audio(file_name)
    display_text(text, text_edit)

def play_audio(file_name):
    os.system(f'start {file_name}')

def display_text(text, text_edit):
    cursor = text_edit.textCursor()
    cursor.movePosition(QTextCursor.End)
    cursor.insertText(text)

def load_story_titles_to_list(list_widget):
    titles = get_story_titles_from_database()
    list_widget.addItems(titles)


import sqlite3
import random

def create_database():
    conn = sqlite3.connect('bed_stories.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Storys (id INTEGER PRIMARY KEY, text TEXT)''')
    conn.commit()
    conn.close()

def add_text(text):
    conn = sqlite3.connect('bed_stories.db')
    c = conn.cursor()

    c.execute("INSERT INTO Storys (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def get_random_text():
    conn = sqlite3.connect('bed_stories.db')
    c = conn.cursor()

    c.execute("SELECT text FROM Storys ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()
    conn.close()

    return result[0] if result else None

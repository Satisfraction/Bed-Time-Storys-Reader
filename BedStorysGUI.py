import sys
from PyQt5 import QtWidgets, QtGui
from Speech import text_to_speech

class BedStorysGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create the "Get Random Text" button and place it on the window
        btn = QtWidgets.QPushButton("Get Random Text", self)
        btn.clicked.connect(self.get_text)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        # Create the label to display the text
        self.label = QtWidgets.QLabel("", self)
        self.label.move(50, 100)

        # Set window geometry and title
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("PyQt Example")
        self.show()

    def get_text(self):
        """
        Get a random text from the database and display it on the label.
        """
        import sqlite3
        conn = sqlite3.connect("bed_storys.db")
        c = conn.cursor()

        # Get a random text from the database
        c.execute("SELECT text FROM Storys ORDER BY RANDOM() LIMIT 1")
        result = c.fetchone()
        conn.close()

        # If a text was found, display it on the label and play it
        if result:
            self.label.setText(result[0])
            self.play_text(result[0])

    def play_text(self, text):
        """
        Play the text using the text-to-speech function.
        """
        text_to_speech(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = BedStorysGUI()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QMainWindow, QListWidget, QPushButton, QApplication, QTextEdit, QWidget, QHBoxLayout, QListWidgetItem, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from functions import get_text_from_database, play_text_with_tts, get_story_titles_from_database


class BedStoriesGUI(QMainWindow):
    font = QFont('Arial', 16)
    button_styles = {
        'play_button': {
            'background-color': 'green',
            'color': 'white',
            'border-radius': '5px'
        },
        'pause_button': {
            'background-color': 'red',
            'color': 'white',
            'border-radius': '5px'
        },
        'resume_button': {
            'background-color': 'blue',
            'color': 'white',
            'border-radius': '5px'
        }
    }

    def __init__(self):
        super().__init__()
        self.media_player = None
        self.titles = self.get_titles_from_database()
        self.initUI()

    def initUI(self):
        self.setStyleSheet('background-color: #EFEFEF;')
        self.setFont(self.font)
        self.setWindowTitle('Mat´s Geschichten Vorleser')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(
            'background-color: #D3D3D3; border: 2px solid black;')
        self.list_widget.setFont(QFont('Arial', 18))
        self.list_widget.itemClicked.connect(self.play_text_from_title)

        for title in self.titles:
            item = QListWidgetItem(title)
            item.setBackground(QtGui.QColor('#F5F5F5'))
            self.list_widget.addItem(item)

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet(
            'background-color: #D3D3D3; border: 2px solid black;')
        self.text_edit.setFont(QFont('Comic Sans MS', 20))
        self.text_edit.setReadOnly(True)

        button_layout = QHBoxLayout()
        self.play_button = QPushButton('Play')
        self.play_button.setStyleSheet(self.get_button_style('play_button'))
        self.play_button.setFont(self.font)
        self.play_button.setMinimumHeight(40)
        self.play_button.clicked.connect(self.play_current_text)

        self.pause_button = QPushButton('Pause')
        self.pause_button.setStyleSheet(self.get_button_style('pause_button'))
        self.pause_button.setFont(self.font)
        self.pause_button.setMinimumHeight(40)
        self.pause_button.clicked.connect(self.pause_audio)

        self.resume_button = QPushButton('Resume')
        self.resume_button.setStyleSheet(self.get_button_style('resume_button'))
        self.resume_button.setFont(self.font)
        self.resume_button.setMinimumHeight(40)
        self.resume_button.clicked.connect(self.resume_audio)

        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.resume_button)

        self.volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.list_widget)
        left_layout.addStretch(1)
        left_layout.addWidget(self.volume_slider)
        self.list_widget.setMinimumHeight(500)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.text_edit)
        right_layout.addStretch(1)
        right_layout.addLayout(button_layout)
        self.text_edit.setMinimumHeight(500)

        self.layout.addLayout(left_layout, 0, 0)
        self.layout.addLayout(right_layout, 0, 1)

        self.setGeometry(500, 300, 1200, 550)
        self.show()

    def get_titles_from_database(self):
        titles = get_story_titles_from_database()
        return titles

    def play_text_from_title(self, item):
        text = get_text_from_database(item.text())
        if text:
            self.current_text = text
            self.text_edit.setText(text)
            self.play_button.setEnabled(True)

    def play_current_text(self):
        self.play_button.setEnabled(False)
        file_name = play_text_with_tts(self.current_text)

        if self.media_player is not None:
            self.media_player.stop()

        self.media_player = QMediaPlayer(self)
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(file_name)))
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

    def get_button_style(self, button_name):
        style = self.button_styles.get(button_name, {})
        return 'background-color: {}; color: {}; border-radius: {};'.format(
            style.get('background-color', ''),
            style.get('color', ''),
            style.get('border-radius', '')
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BedStoriesGUI()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from ui.home_screen import HomeScreen
from ui.meeting_form import MeetingForm

class SmartMeetingNotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Meeting Notes")
        self.setGeometry(100, 100, 1000, 720)
        self.setMinimumSize(800, 600)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.dark_mode = False

        self.home = HomeScreen(self.load_meeting_form, self.toggle_theme)
        self.stack.addWidget(self.home)

        self.apply_light_theme()

    def load_meeting_form(self, meeting_type):
        self.form = MeetingForm(meeting_type, self.show_home)
        self.stack.addWidget(self.form)
        self.stack.setCurrentWidget(self.form)

    def show_home(self):
        self.stack.setCurrentWidget(self.home)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_light_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6fc;
                color: #111;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                color: #111;
            }
            QTextEdit {
                background-color: #fff;
                color: #111;
            }
            QPushButton {
                background-color: #3a4fa0;
                color: white;
            }
            QPushButton:hover {
                background-color: #2e3f85;
            }
            QDateEdit, QTimeEdit {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px;
            }
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2c2c2c;
                color: #eee;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                color: #eee;
            }
            QTextEdit {
                background-color: #3d3d3d;
                color: #fff;
            }
            QPushButton {
                background-color: #6b63ff;
                color: white;
            }
            QPushButton:hover {
                background-color: #5a52e0;
            }
            QDateEdit, QTimeEdit {
                background-color: #3d3d3d;
                color: #eee;
                border: 1px solid #666;
                border-radius: 6px;
                padding: 4px;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartMeetingNotesApp()
    window.show()
    sys.exit(app.exec_())

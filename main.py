# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from ui.home_screen import HomeScreen
from ui.meeting_form import MeetingForm

class SmartMeetingNotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Meeting Notes")
        self.setGeometry(100, 100, 1200, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home = HomeScreen(self.load_meeting_form, self.toggle_theme)
        self.stack.addWidget(self.home)

        self.dark_mode = False
        self.apply_light_theme()

    def load_meeting_form(self, meeting_type):
        form = MeetingForm(meeting_type, self.show_home)
        self.stack.addWidget(form)
        self.stack.setCurrentWidget(form)

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
                background-color: #f5f5f5;
                color: #000;
            }
            QPushButton {
                background-color: #4f46e5;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #fff;
            }
            QPushButton {
                background-color: #6b63ff;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a52e0;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartMeetingNotesApp()
    window.show()
    sys.exit(app.exec_())

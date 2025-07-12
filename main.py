import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLabel

class MeetingNotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meeting Notes App")
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.label = QLabel("📝 Meeting Notes")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.button = QPushButton("Generate MoM")
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeetingNotesApp()
    window.show()
    sys.exit(app.exec_())

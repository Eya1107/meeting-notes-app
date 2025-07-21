from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self, load_meeting_form_callback, toggle_theme_callback):
        super().__init__()
        self.load_meeting_form_callback = load_meeting_form_callback
        self.toggle_theme_callback = toggle_theme_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("📋 Smart Meeting Notes")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #3a4fa0; margin-bottom: 40px;")

        layout.addWidget(title)
        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        meeting_types = [
            "Client Meeting",
            "Team Meeting",
            "Follow-up Meeting"
        ]

        for mtype in meeting_types:
            btn = QPushButton(mtype)
            btn.setFixedSize(260, 48)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    background-color: #3a4fa0;
                    color: white;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2e3f85;
                }
            """)
            btn.clicked.connect(lambda checked, t=mtype: self.load_meeting_form_callback(t))
            layout.addWidget(btn, alignment=Qt.AlignCenter)
            layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        toggle_btn = QPushButton("🌓 Toggle Theme")
        toggle_btn.setFixedSize(160, 38)
        toggle_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #d9e1ff;
                color: #3a4fa0;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c7d2ff;
            }
        """)
        toggle_btn.clicked.connect(self.toggle_theme_callback)
        layout.addWidget(toggle_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

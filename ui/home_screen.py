# ui/home_screen.py

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
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Meeting type buttons
        meeting_types = [
            "Client Meeting",
            "Team Meeting",
            "Follow-up Meeting"
        ]

        for mtype in meeting_types:
            btn = QPushButton(mtype)
            btn.setFixedWidth(250)
            btn.setStyleSheet("font-size: 16px;")
            btn.clicked.connect(lambda checked, t=mtype: self.load_meeting_form_callback(t))
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Toggle theme button
        toggle_btn = QPushButton("🌓 Toggle Theme")
        toggle_btn.setFixedWidth(180)
        toggle_btn.clicked.connect(self.toggle_theme_callback)
        layout.addWidget(toggle_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)  
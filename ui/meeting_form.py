# ui/meeting_form.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt

class MeetingForm(QWidget):
    def __init__(self, meeting_type, go_back_callback):
        super().__init__()
        self.meeting_type = meeting_type
        self.go_back_callback = go_back_callback
        self.init_ui()

    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel(f"{self.meeting_type}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        self.fields = {}

        def add_field(label_text):
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; font-size: 15px; margin-top: 10px;")
            text_edit = QTextEdit()
            text_edit.setPlaceholderText(f"Write {label_text.lower()} here...")
            text_edit.setFixedHeight(100)
            text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #ffffff;
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 14px;
                }
            """)
            layout.addWidget(label)
            layout.addWidget(text_edit)
            self.fields[label_text] = text_edit

        # Champs de base
        add_field("Date & Time")
        add_field("Participants")

        if self.meeting_type == "Client Meeting":
            add_field("Client Objectives")
            add_field("Key Discussions")
            add_field("Decisions")
            add_field("Actions / Emails")
            add_field("Next Meeting Date")

        elif self.meeting_type == "Team Meeting":
            add_field("Agenda")
            add_field("Task Progress")
            add_field("Remarks")
            add_field("Decisions")
            add_field("Action Items")
            add_field("Next Meeting Date")

        elif self.meeting_type == "Follow-up Meeting":
            add_field("Previous Tasks & Progress")
            add_field("Problems Encountered")
            add_field("Decisions / Resolutions")
            add_field("Remaining Actions")
            add_field("Next Step")

        # Case en plus pour tous les types de réunion
        add_field("Other Notes")

        # Boutons navigation
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet("padding: 6px 12px; font-weight: bold;")
        back_btn.clicked.connect(self.go_back_callback)

        save_btn = QPushButton("💾 Save (to implement)")
        save_btn.setStyleSheet("padding: 6px 12px;")

        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)

        layout.addSpacing(15)
        layout.addLayout(btn_layout)

        scroll.setWidget(container)
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

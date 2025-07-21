from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QHBoxLayout, QGridLayout, QDateEdit, QTimeEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QDate, QTime

from ai_model import generate_summary, generate_email  # ⬅️ Import modèle IA

class MeetingForm(QWidget):
    def __init__(self, meeting_type, go_back_callback):
        super().__init__()
        self.meeting_type = meeting_type
        self.go_back_callback = go_back_callback
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(25)

        # Header
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(90, 35)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a4fa0;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2e3f85;
            }
        """)
        back_btn.clicked.connect(self.go_back_callback)
        header_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        title = QLabel(f"{self.meeting_type}")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #2e3f85;")
        header_layout.addStretch()
        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Grid Layout
        form_layout = QGridLayout()
        form_layout.setSpacing(20)

        def create_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight: 600; font-size: 15px;")
            return lbl

        def create_textedit(placeholder, height=70):
            te = QTextEdit()
            te.setPlaceholderText(placeholder)
            te.setFixedHeight(height)
            te.setStyleSheet("""
                QTextEdit {
                    background-color: #fdfdfd;
                    border: 1px solid #bbb;
                    border-radius: 6px;
                    padding: 6px;
                    font-size: 14px;
                }
                QTextEdit:focus {
                    border: 1px solid #3a4fa0;
                }
            """)
            return te

        self.fields = {}

        left_fields = [
            ("Project Name:", 70),
            ("Participants:", 80),
            ("Actions:", 80),
            ("Decisions:", 80),
        ]

        right_fields = [
            ("Remarks:", 80),
            ("Next Meeting:", 80),
            ("Reminder Note:", 80),
        ]

        for i, (label, height) in enumerate(left_fields):
            form_layout.addWidget(create_label(label), i, 0)
            widget = create_textedit(f"Write {label.lower()[:-1]} here...", height)
            self.fields[label[:-1]] = widget
            form_layout.addWidget(widget, i, 1)

        for i, (label, height) in enumerate(right_fields):
            form_layout.addWidget(create_label(label), i, 2)
            widget = create_textedit(f"Write {label.lower()[:-1]} here...", height)
            self.fields[label[:-1]] = widget
            form_layout.addWidget(widget, i, 3)

        # Reminder Date & Time
        form_layout.addWidget(create_label("Reminder Date & Time:"), len(right_fields), 2)

        reminder_layout = QHBoxLayout()
        self.reminder_date = QDateEdit()
        self.reminder_date.setCalendarPopup(True)
        self.reminder_date.setDate(QDate.currentDate())
        self.reminder_date.setFixedWidth(140)

        self.reminder_time = QTimeEdit()
        self.reminder_time.setTime(QTime.currentTime())
        self.reminder_time.setFixedWidth(110)

        reminder_layout.addWidget(self.reminder_date)
        reminder_layout.addWidget(self.reminder_time)

        reminder_container = QWidget()
        reminder_container.setLayout(reminder_layout)
        form_layout.addWidget(reminder_container, len(right_fields), 3)

        main_layout.addLayout(form_layout)

        # Bottom Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        style_btn = """
            QPushButton {
                background-color: #3a4fa0;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #2e3f85;
            }
        """

        btn_generate_summary = QPushButton("Generate Summary")
        btn_generate_summary.setStyleSheet(style_btn)
        btn_generate_summary.setFixedSize(160, 40)
        btn_generate_summary.clicked.connect(self.handle_generate_summary)

        btn_prepare_mail = QPushButton("Prepare Email")
        btn_prepare_mail.setStyleSheet(style_btn)
        btn_prepare_mail.setFixedSize(160, 40)
        btn_prepare_mail.clicked.connect(self.handle_prepare_email)

        btn_generate_mom = QPushButton("Generate MoM")
        btn_generate_mom.setStyleSheet(style_btn)
        btn_generate_mom.setFixedSize(160, 40)

        btn_layout.addWidget(btn_generate_summary)
        btn_layout.addWidget(btn_prepare_mail)
        btn_layout.addWidget(btn_generate_mom)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def collect_form_data(self):
        data = {label: widget.toPlainText() for label, widget in self.fields.items()}
        data["Reminder Date"] = self.reminder_date.date().toString("yyyy-MM-dd")
        data["Reminder Time"] = self.reminder_time.time().toString("HH:mm")
        return data

    def show_output(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setTextInteractionFlags(Qt.TextSelectableByMouse)
        msg.setStyleSheet("font-size: 14px;")
        msg.setText(text)
        msg.exec_()

    def handle_generate_summary(self):
        data = self.collect_form_data()
        summary = generate_summary(data)
        self.show_output("Meeting Summary", summary)

    def handle_prepare_email(self):
        data = self.collect_form_data()
        email = generate_email(data)
        self.show_output("Prepared Email", email)

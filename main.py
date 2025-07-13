import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QListWidget, QPushButton, QTabWidget, QLabel, 
                             QSplitter, QFrame, QToolBar, QCalendarWidget, QStackedWidget,
                             QAction)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

class SmartNotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Meeting Notes")
        self.setGeometry(100, 100, 1400, 900)
        self.dark_mode = False
        self.meeting_data = {}
        self.initUI()
        self.apply_light_theme()

    def initUI(self):
        # Menu Bar
        menubar = self.menuBar()
        view_menu = menubar.addMenu('View')
        
        # Theme toggle action
        self.theme_action = QAction('Dark Mode', self)
        self.theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.theme_action)

        # Main widget
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Left sidebar - Agenda + Notes list
        left_sidebar = QFrame()
        left_sidebar.setFixedWidth(300)
        left_layout = QVBoxLayout(left_sidebar)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Calendar Widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.on_date_selected)
        
        # Meeting list for selected date
        self.meeting_list = QListWidget()
        self.meeting_list.itemClicked.connect(self.show_meeting_details)

        # New meeting button
        new_meeting_btn = QPushButton("New Meeting")
        new_meeting_btn.setIcon(QIcon.fromTheme("document-new"))
        new_meeting_btn.clicked.connect(self.new_meeting)

        left_layout.addWidget(self.calendar)
        left_layout.addWidget(new_meeting_btn)
        left_layout.addWidget(QLabel("Meetings:"))
        left_layout.addWidget(self.meeting_list)

        # Right area - Stacked widget for editor/viewer
        self.stacked_widget = QStackedWidget()

        # Editor view
        self.editor_view = QWidget()
        editor_layout = QVBoxLayout(self.editor_view)
        
        self.note_editor = QTextEdit()
        self.note_editor.setPlaceholderText("Write your meeting notes here...")
        
        analyze_btn = QPushButton("Analyze Notes")
        analyze_btn.clicked.connect(self.analyze_notes)
        
        editor_layout.addWidget(self.note_editor)
        editor_layout.addWidget(analyze_btn)

        # Viewer view
        self.viewer_view = QWidget()
        viewer_layout = QVBoxLayout(self.viewer_view)
        
        self.viewer_tabs = QTabWidget()
        
        # Agenda tab
        agenda_tab = QWidget()
        agenda_layout = QVBoxLayout(agenda_tab)
        self.agenda_display = QTextEdit()
        self.agenda_display.setReadOnly(True)
        agenda_layout.addWidget(self.agenda_display)

        # Email tab
        email_tab = QWidget()
        email_layout = QVBoxLayout(email_tab)
        self.email_display = QTextEdit()
        email_layout.addWidget(self.email_display)

        # Highlights tab
        highlights_tab = QWidget()
        highlights_layout = QVBoxLayout(highlights_tab)
        self.highlights_display = QTextEdit()
        self.highlights_display.setReadOnly(True)
        highlights_layout.addWidget(self.highlights_display)

        self.viewer_tabs.addTab(agenda_tab, "Agenda")
        self.viewer_tabs.addTab(email_tab, "Emails")
        self.viewer_tabs.addTab(highlights_tab, "Highlights")
        
        viewer_layout.addWidget(self.viewer_tabs)

        # Add views to stack
        self.stacked_widget.addWidget(self.editor_view)
        self.stacked_widget.addWidget(self.viewer_view)
        self.stacked_widget.setCurrentIndex(0)

        # Assemble main layout
        main_layout.addWidget(left_sidebar)
        main_layout.addWidget(self.stacked_widget)

        self.setCentralWidget(main_widget)

    def on_date_selected(self, date):
        """When a date is selected in calendar"""
        self.current_date = date.toString(Qt.ISODate)
        self.update_meeting_list(date)

    def update_meeting_list(self, date):
        """Update meeting list for selected date"""
        self.meeting_list.clear()
        if self.current_date in self.meeting_data:
            for meeting in self.meeting_data[self.current_date]:
                self.meeting_list.addItem(meeting['title'])

    def new_meeting(self):
        """Start a new meeting"""
        self.stacked_widget.setCurrentIndex(0)
        self.note_editor.clear()

    def show_meeting_details(self, item):
        """Show saved meeting details"""
        meeting_title = item.text()
        if self.current_date in self.meeting_data:
            for meeting in self.meeting_data[self.current_date]:
                if meeting['title'] == meeting_title:
                    self.agenda_display.setPlainText(meeting.get('agenda', ''))
                    self.email_display.setPlainText(meeting.get('email', ''))
                    self.highlights_display.setPlainText(meeting.get('highlights', ''))
                    self.stacked_widget.setCurrentIndex(1)
                    break

    def analyze_notes(self):
        """Analyze current notes and save meeting"""
        if not self.note_editor.toPlainText():
            return
            
        meeting_title = f"Meeting {QDate.currentDate().toString(Qt.DefaultLocaleShortDate)}"
        meeting_data = {
            'title': meeting_title,
            'notes': self.note_editor.toPlainText(),
            'agenda': "Extracted dates:\n- 2023-11-15: Project review",
            'email': "Draft email content...",
            'highlights': "Key decisions:\n- Use PyQt5 for UI"
        }
        
        if self.current_date not in self.meeting_data:
            self.meeting_data[self.current_date] = []
        self.meeting_data[self.current_date].append(meeting_data)
        
        self.meeting_list.addItem(meeting_title)
        self.show_meeting_details(self.meeting_list.item(self.meeting_list.count()-1))

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.dark_mode = not self.dark_mode
        self.theme_action.setText('Light Mode' if self.dark_mode else 'Dark Mode')
        if self.dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_light_theme(self):
        """Modern light theme with better contrast"""
        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.WindowText, Qt.black)
        light_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ToolTipBase, Qt.white)
        light_palette.setColor(QPalette.ToolTipText, Qt.black)
        light_palette.setColor(QPalette.Text, Qt.black)
        light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ButtonText, Qt.black)
        light_palette.setColor(QPalette.BrightText, Qt.red)
        light_palette.setColor(QPalette.Highlight, QColor(100, 149, 237))
        light_palette.setColor(QPalette.HighlightedText, Qt.white)
        
        self.setPalette(light_palette)
        QApplication.setPalette(light_palette)
        
        self.setStyleSheet("""
            QMainWindow, QWidget, QDialog {
                background-color: #f0f0f0;
                color: #000000;
            }
            QTextEdit, QListWidget, QCalendarWidget, QTabWidget {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #d0d0d0;
            }
            QPushButton {
                background-color: #4f46e5;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QTabBar::tab {
                background: #e0e0e0;
                color: #000000;
                padding: 5px 10px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-bottom: 2px solid #4f46e5;
            }
        """)

    def apply_dark_theme(self):
        """Sophisticated dark theme"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.black)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        
        self.setPalette(dark_palette)
        QApplication.setPalette(dark_palette)
        
        self.setStyleSheet("""
            QMainWindow, QWidget, QDialog {
                background-color: #353535;
                color: #ffffff;
            }
            QTextEdit, QListWidget, QCalendarWidget, QTabWidget {
                background-color: #252525;
                color: #ffffff;
                border: 1px solid #444444;
            }
            QPushButton {
                background-color: #6b63ff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #5a52e0;
            }
            QTabBar::tab {
                background: #444444;
                color: #ffffff;
                padding: 5px 10px;
            }
            QTabBar::tab:selected {
                background: #252525;
                border-bottom: 2px solid #6b63ff;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "Inter")
    font.setPointSize(10)
    app.setFont(font)
    
    window = SmartNotesApp()
    window.show()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from views.profile_ui import Ui_StreamingProfileDialog

class StreamingProfileDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StreamingProfileDialog()
        self.ui.setupUi(self)
        
        # Set window flags for custom styling
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        # Apply theme
        from utils.theme_manager import ThemeManager
        ThemeManager().apply_theme_to_profile_dialog(self)
        
        # Connect button signals
        self.ui.saveButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)
        
        # Set object names for QSS styling
        self.setObjectName("StreamingProfileDialog")
        self.ui.saveButton.setObjectName("saveButton")
        self.ui.cancelButton.setObjectName("cancelButton")
        
        # Remove window title as we're using frameless window
        self.setWindowTitle("")
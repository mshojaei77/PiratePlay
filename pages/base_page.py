from PyQt5.QtWidgets import QWidget

class BasePageWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._is_active = False
        
    def on_page_activate(self):
        """Called when page becomes active"""
        self._is_active = True
        
    def on_page_deactivate(self):
        """Called when page becomes inactive"""
        self._is_active = False
        
    @property
    def is_active(self):
        """Returns whether the page is currently active"""
        return self._is_active
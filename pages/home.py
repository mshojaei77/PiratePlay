from pages.base_page import BasePageWidget
from views.home_ui import Ui_HomeWidget

class HomeWidget(BasePageWidget):
    def __init__(self, app):
        super().__init__(app)
        self.ui = Ui_HomeWidget()
        self.ui.setupUi(self)
        
    def on_page_activate(self):
        super().on_page_activate()
        # Add page-specific activation logic here
        
    def on_page_deactivate(self):
        super().on_page_deactivate()
        # Add page-specific cleanup logic here

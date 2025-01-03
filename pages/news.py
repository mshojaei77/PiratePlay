from pages.base_page import BasePageWidget
from views.news_ui import Ui_NewsWidget

class NewsWidget(BasePageWidget):
    def __init__(self, app):
        super().__init__(app)
        self.ui = Ui_NewsWidget()
        self.ui.setupUi(self)

    def on_page_activate(self):
        super().on_page_activate()
        # Add page-specific activation logic here
        
    def on_page_deactivate(self):
        super().on_page_deactivate()
        # Add page-specific cleanup logic here
from views.search_results_ui import Ui_SearchResultsWidget
from pages.base_page import BasePageWidget

class SearchResultsWidget(BasePageWidget):
    def __init__(self,app):
        super().__init__(app)
        self.ui = Ui_SearchResultsWidget()
        self.ui.setupUi(self)
        
    def on_page_activate(self):
        super().on_page_activate()
        # Add page-specific activation logic here
        
    def on_page_deactivate(self):
        super().on_page_deactivate()
        # Add page-specific cleanup logic here

    def update_search(self, search_text):
        """Update the search results for the given search text"""
        self.ui.results_label.setText(f"Search Results for: {search_text}")
        # Implement your search logic here
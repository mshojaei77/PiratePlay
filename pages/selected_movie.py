from PyQt5.QtWidgets import QWidget
from views.selected_movie_ui import Ui_SelectedMovie

class SelectedMovie(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SelectedMovie()
        self.ui.setupUi(self)
        self.current_movie = None

    def show_selected_movie(self, movie_name):
        print(movie_name)
        pass


    def on_page_activate(self):
        """Called when page becomes active"""
        pass

    def on_page_deactivate(self):
        """Called when page becomes inactive"""
        pass

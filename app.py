from PyQt5.QtWidgets import QApplication
from pages.main import MainWindow
import sys
import resources_rc  # Add this line

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
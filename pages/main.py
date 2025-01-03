from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from views.main_ui import Ui_MainWindow
from utils.theme_manager import ThemeManager
from pages.settings import SettingsWidget
from pages.home import HomeWidget
from pages.discover import DiscoverWidget
from pages.collections import CollectionsWidget
from pages.downloads import DownloadsWidget
from pages.player import PlayerWidget
from pages.news import NewsWidget
from dialogs.profile import StreamingProfileDialog
from pages.search_results import SearchResultsWidget
import functools

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Initialize UI components
        self.theme_manager.initialize_landing_page(self)
        
        # Make window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Set up navigation mapping BEFORE initializing pages
        self.nav_button_mapping = {
            self.ui.navigationHomeButton: 'home',
            self.ui.navigationDiscoverButton: 'discover',
            self.ui.navigationCollectionsButton: 'collections',
            self.ui.navigationDownloadsButton: 'downloads',
            self.ui.navigationPlayerButton: 'player',
            self.ui.navigationNewsButton: 'news',
            self.ui.navigationSettingsButton: 'settings'
        }
        
        # Initialize pages
        self._initialize_pages()
        
        # Connect signals
        self._connect_signals()
    
    def _initialize_pages(self):
        """Initialize all page widgets"""
        # Create all pages with self as parent
        self.current_page = None
        self.pages = {
            'home': HomeWidget(self),
            'discover': DiscoverWidget(self),
            'collections': CollectionsWidget(self),
            'downloads': DownloadsWidget(self),
            'player': PlayerWidget(self),
            'news': NewsWidget(self),
            'settings': SettingsWidget(self),
            'search_results': SearchResultsWidget(self)
        }
        
        # Add pages to stack and store indices
        self.page_indices = {}
        for i, (name, widget) in enumerate(self.pages.items()):
            self.ui.stackedWidget.addWidget(widget)
            self.page_indices[name] = i + 2
            
        # Set initial page
        self._navigate_to_page('home')
    
    def _connect_signals(self):
        """Connect all button signals"""
        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button.clicked.connect(self._toggle_maximize)
        self.close_button.clicked.connect(self.close)
        self.ui.themeToggleButton.clicked.connect(self._toggle_theme)
        self.ui.userProfileButton.clicked.connect(self._show_profile_dialog)
        
        # Fix navigation button connections
        for button, page_name in self.nav_button_mapping.items():
            # Use functools.partial instead of lambda to avoid late binding issues
            button.clicked.connect(self._create_navigation_handler(page_name))
        
        # Add search input connection
        self.ui.globalSearchInput.textChanged.connect(self._handle_search)
    
    def _create_navigation_handler(self, page_name):
        """Create a proper navigation handler for each button"""
        return lambda: self._navigate_to_page(page_name)
    
    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def _toggle_theme(self):
        # Toggle theme and get new colors
        self.theme_manager.toggle_theme()
        
        # Update all icons and styles
        self.theme_manager.apply_theme_to_landing_page(self)
        
        # Explicitly update window controls
        self.theme_manager.apply_theme_to_window_controls(
            self.minimize_button,
            self.maximize_button,
            self.close_button
        )
        
        # Update search
        self.theme_manager.apply_theme_to_search(self.ui.globalSearchInput)
    
    def _navigate_to_page(self, page_name):
        """Navigate to the specified page with proper state management"""
        try:
            if page_name not in self.pages:
                print(f"Error: Page '{page_name}' not found")
                return
                
            if self.current_page == page_name:
                return
                
            # Deactivate current page if exists
            if self.current_page and self.current_page in self.pages:
                self.pages[self.current_page].on_page_deactivate()
                
            # Update button states
            for button, mapped_page in self.nav_button_mapping.items():
                button.setChecked(mapped_page == page_name)
            
            # Activate new page
            self.pages[page_name].on_page_activate()
            self.current_page = page_name
            
            # Show the selected page
            self.ui.stackedWidget.setCurrentIndex(self.page_indices[page_name])
            
        except Exception as e:
            print(f"Error navigating to page '{page_name}': {str(e)}")
        
    def _show_profile_dialog(self):
        """Show the user profile dialog"""
        dialog = StreamingProfileDialog()
        dialog.exec_()
        
    def _handle_search(self, search_text):
        """Handle search input changes"""
        if search_text.strip():
            # Update search results page with new search text
            self.pages['search_results'].update_search(search_text)
            # Navigate to search results page
            self._navigate_to_page('search_results')
        else:
            # If search is cleared, go back to previous page or home
            if self.current_page == 'search_results':
                self._navigate_to_page('home')
        

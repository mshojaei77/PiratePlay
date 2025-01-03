from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, QHBoxLayout
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ThemeColors:
    text: str
    background: str
    secondary_background: str
    hover: str
    active: str
    border: str

class ThemeManager:
    ICON_SIZES = {
        'window_controls': QSize(16, 16),
        'navigation': QSize(30, 30),
        'app_icon': QSize(30, 30),
        'search': QSize(16, 16),
        'control_buttons': QSize(20, 20)
    }
    
    FONT_SIZES = {
        'title': '14px',
        'navigation': '13px',
        'search': '13px',
        'content': '13px'
    }

    DARK_THEME = ThemeColors(
        text="#FFFFFF",
        background="#1E1E1E",
        secondary_background="#333333",
        hover="rgba(255, 255, 255, 0.1)",
        active="rgba(255, 255, 255, 0.15)",
        border="rgba(255, 255, 255, 0.1)"
    )
    
    LIGHT_THEME = ThemeColors(
        text="#000000",
        background="#FFFFFF",
        secondary_background="#F5F5F5",
        hover="rgba(0, 0, 0, 0.1)",
        active="rgba(0, 0, 0, 0.15)",
        border="rgba(0, 0, 0, 0.1)"
    )

    def __init__(self):
        self.is_dark_mode = True
        self.current_theme = self.DARK_THEME
        self.icon_cache = {}  # Cache for colored icons

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.current_theme = self.DARK_THEME if self.is_dark_mode else self.LIGHT_THEME
        # Clear the icon cache to force recreation of icons with new colors
        self.icon_cache.clear()
        return self.current_theme

    @staticmethod
    def create_colored_icon(path: str, color: str) -> QIcon:
        """Create a colored version of an SVG icon"""
        try:
            with open(path, 'r') as file:
                svg_content = file.read()
                # Replace all possible color attributes
                replacements = [
                    # Current color replacements
                    ('fill="currentColor"', f'fill="{color}"'),
                    ('stroke="currentColor"', f'stroke="{color}"'),
                    
                    # Common color names
                    ('fill="black"', f'fill="{color}"'),
                    ('stroke="black"', f'stroke="{color}"'),
                    ('fill="white"', f'fill="{color}"'),
                    ('stroke="white"', f'stroke="{color}"'),
                    
                    # Hex colors
                    ('fill="#000000"', f'fill="{color}"'),
                    ('stroke="#000000"', f'stroke="{color}"'),
                    ('fill="#000"', f'fill="{color}"'),
                    ('stroke="#000"', f'stroke="{color}"'),
                    ('fill="#020202"', f'fill="{color}"'),
                    ('fill="#0F0F0F"', f'fill="{color}"'),
                    ('fill="#0F1729"', f'fill="{color}"'),
                    ('fill="#292929"', f'fill="{color}"'),
                    
                    # Additional attributes
                    ('color="#000000"', f'color="{color}"'),
                    ('color="#000"', f'color="{color}"'),
                    
                    # Style-based colors
                    ('style="fill:#000000"', f'style="fill:{color}"'),
                    ('style="fill:#000"', f'style="fill:{color}"'),
                    ('style="stroke:#000000"', f'style="stroke:{color}"'),
                    ('style="stroke:#000"', f'style="stroke:{color}"'),
                    
                    # Partial style replacements
                    ('fill:#000000', f'fill:{color}'),
                    ('fill:#000', f'fill:{color}'),
                    ('stroke:#000000', f'stroke:{color}'),
                    ('stroke:#000', f'stroke:{color}'),
                    ('fill:#020202', f'fill:{color}'),
                    ('fill:#0F0F0F', f'fill:{color}'),
                    ('fill:#0F1729', f'fill:{color}'),
                    ('fill:#292929', f'fill:{color}'),
                    
                    # Add specific stroke color for news.svg
                    ('stroke="#292929"', f'stroke="{color}"'),
                ]
                
                for old, new in replacements:
                    svg_content = svg_content.replace(old, new)
                
                # Debug output to verify replacement
                if "news.svg" in path:
                    #print(f"Modified SVG content: {svg_content}")
                    pass
                    
                pixmap = QPixmap()
                pixmap.loadFromData(svg_content.encode('utf-8'))
                
                if pixmap.isNull():
                    print(f"Warning: Failed to create colored icon from {path}")
                    return QIcon(path)
                    
                return QIcon(pixmap)
        except Exception as e:
            print(f"Error creating colored icon: {e}")
            return QIcon(path)

    def get_stylesheet(self) -> str:
        """Load stylesheet based on current theme from QSS files"""
        try:
            theme_file = "styles/dark.qss" if self.is_dark_mode else "styles/light.qss"
            with open(theme_file, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
            return ""

    def apply_theme_to_button(self, button: QPushButton, icon_path: str, 
                            size: QSize = None, is_nav_button: bool = False) -> None:
        """Apply theme styling and icon to a button"""
        button.setIcon(self.get_colored_icon(icon_path))
        button.setIconSize(size or self.ICON_SIZES['control_buttons'])
        button.setText("")
        
        # Add margin for navigation buttons
        nav_padding = "8px" if is_nav_button else "0px"
        
        base_style = f"""
            QPushButton {{ 
                border: none; 
                background: none; 
                padding: {nav_padding}; 
                margin: 2px 8px; 
            }}
            QPushButton:hover {{ 
                background-color: {self.current_theme.hover};
                border-radius: 4px;
            }}
        """

        button.setStyleSheet(base_style)

    def get_colored_icon(self, path: str) -> QIcon:
        """Get or create a colored icon from cache"""
        # Use white for dark mode, black for light mode
        icon_color = "#FFFFFF" if self.is_dark_mode else "#000000"
        cache_key = f"{path}_{icon_color}"
        if cache_key not in self.icon_cache:
            self.icon_cache[cache_key] = self.create_colored_icon(path, icon_color)
        return self.icon_cache[cache_key]

    def apply_theme_to_window_controls(self, minimize_btn: QPushButton, 
                                     maximize_btn: QPushButton, 
                                     close_btn: QPushButton) -> None:
        """Apply theme to window control buttons"""
        for btn, icon_name in [(minimize_btn, "minimize"), 
                             (maximize_btn, "maximize"), 
                             (close_btn, "close")]:
            self.apply_theme_to_button(btn, f"./assets/icons/{icon_name}.svg")
            
        # Special styles for window control buttons
        minimize_btn.setStyleSheet(minimize_btn.styleSheet() + """
            QPushButton:hover { 
                background-color: rgba(255, 255, 0, 0.7);
                border-radius: 4px;
            }
        """)
        
        maximize_btn.setStyleSheet(maximize_btn.styleSheet() + """
            QPushButton:hover { 
                background-color: rgba(0, 255, 0, 0.7);
                border-radius: 4px;
            }
        """)
        
        close_btn.setStyleSheet(close_btn.styleSheet() + """
            QPushButton:hover { 
                background-color: rgba(255, 0, 0, 0.7);
                border-radius: 4px;
            }
        """)

    def apply_theme_to_search(self, search_input: QLineEdit) -> None:
        """Apply theme to search input"""
        # Remove all existing actions first
        while search_input.actions():
            search_input.removeAction(search_input.actions()[0])
        
        # Add new search icon
        search_icon = self.get_colored_icon("./assets/icons/search.svg")
        search_input.addAction(search_icon, QLineEdit.LeadingPosition)

    def apply_theme_to_landing_page(self, landing_page) -> None:
        """Apply theme to all elements in the landing page"""
        # Apply stylesheet
        landing_page.setStyleSheet(self.get_stylesheet())
        
        # Define navigation buttons
        nav_buttons = {
            landing_page.ui.navigationHomeButton: "home",
            landing_page.ui.navigationDiscoverButton: "discover",
            landing_page.ui.navigationCollectionsButton: "collections",
            landing_page.ui.navigationDownloadsButton: "downloads",
            landing_page.ui.navigationPlayerButton: "player",
            landing_page.ui.navigationNewsButton: "news",
            landing_page.ui.navigationSettingsButton: "settings"
        }
        
        # Apply theme to navigation buttons
        for button, icon_name in nav_buttons.items():
            button.setCheckable(True)
            self.apply_theme_to_button(
                button,
                f"./assets/icons/{icon_name}.svg",
                self.ICON_SIZES['navigation'],
                is_nav_button=True
            )
        
        # Apply theme to control buttons
        control_buttons = {
            landing_page.ui.userProfileButton: "profile"
        }
        
        # Handle theme toggle button separately
        self.apply_theme_to_button(
            landing_page.ui.themeToggleButton,
            "./assets/icons/mode-light.svg" if self.is_dark_mode else "./assets/icons/mode-dark.svg"
        )
        
        for button, icon_name in control_buttons.items():
            self.apply_theme_to_button(
                button,
                f"./assets/icons/{icon_name}.svg"
            )
        
        # Apply theme to window controls
        self.apply_theme_to_window_controls(
            landing_page.minimize_button,
            landing_page.maximize_button,
            landing_page.close_button
        )
        
        # Apply theme to search
        self.apply_theme_to_search(landing_page.ui.globalSearchInput)

    def initialize_landing_page(self, landing_page) -> None:
        """Initialize all UI components for the landing page"""
        # Create window control buttons first
        landing_page.minimize_button = self._create_window_button("minimize")
        landing_page.maximize_button = self._create_window_button("maximize")
        landing_page.close_button = self._create_window_button("close")
        
        # Initialize components
        self._initialize_title_bar(landing_page)
        self._initialize_navigation_buttons(landing_page)
        self._initialize_control_buttons(landing_page)
        
        # Apply initial theme
        self.apply_theme_to_landing_page(landing_page)

    def _initialize_title_bar(self, landing_page) -> None:
        """Initialize title bar components"""
        # Create container widget for icons
        landing_page.title_icons = QWidget()
        title_icons_layout = QHBoxLayout()
        title_icons_layout.setContentsMargins(0, 0, 0, 0)
        title_icons_layout.setSpacing(4)
        landing_page.title_icons.setLayout(title_icons_layout)
        
        # Add app icon
        landing_page.app_icon = QLabel()
        icon_path = "./assets/icons/app_icon.svg"
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Warning: Could not load icon from {icon_path}")
        else:
            landing_page.app_icon.setPixmap(pixmap.scaled(
                self.ICON_SIZES['app_icon'].width(),
                self.ICON_SIZES['app_icon'].height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
        title_icons_layout.addWidget(landing_page.app_icon)
        
        # Add title label
        landing_page.title_label = QLabel("Pirate Play")
        landing_page.title_label.setObjectName("titleLabel")
        landing_page.title_label.setStyleSheet(f"""
            QLabel {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: {self.FONT_SIZES['title']};
                font-weight: 800;
                margin-left: 4px;
                margin-right: 8px;
            }}
        """)
        title_icons_layout.addWidget(landing_page.title_label)
        
        # Enable mouse tracking for window dragging
        landing_page.title_icons.mousePressEvent = lambda e: self._handle_title_press(e, landing_page)
        landing_page.title_icons.mouseMoveEvent = lambda e: self._handle_title_move(e, landing_page)
        
        # Enable mouse tracking for child widgets
        landing_page.app_icon.mousePressEvent = lambda e: self._handle_title_press(e, landing_page)
        landing_page.app_icon.mouseMoveEvent = lambda e: self._handle_title_move(e, landing_page)
        landing_page.title_label.mousePressEvent = lambda e: self._handle_title_press(e, landing_page)
        landing_page.title_label.mouseMoveEvent = lambda e: self._handle_title_move(e, landing_page)
        
        # Add widgets to titlebar layout
        landing_page.ui.horizontalLayout_TITLEBAR.addWidget(landing_page.title_icons)
        landing_page.ui.horizontalLayout_TITLEBAR.addStretch()
        landing_page.ui.horizontalLayout_TITLEBAR.addWidget(landing_page.minimize_button)
        landing_page.ui.horizontalLayout_TITLEBAR.addWidget(landing_page.maximize_button)
        landing_page.ui.horizontalLayout_TITLEBAR.addWidget(landing_page.close_button)

    def _handle_title_press(self, event, landing_page):
        """Handle mouse press event on title bar"""
        if event.button() == Qt.LeftButton:
            landing_page._drag_pos = event.globalPos() - landing_page.pos()
            event.accept()

    def _handle_title_move(self, event, landing_page):
        """Handle mouse move event on title bar"""
        if hasattr(landing_page, '_drag_pos'):
            if event.buttons() == Qt.LeftButton:
                landing_page.move(event.globalPos() - landing_page._drag_pos)
                event.accept()

    def _create_window_button(self, button_type: str) -> QPushButton:
        """Create a window control button"""
        button = QPushButton()
        button.setFixedSize(45, 30)  # Increased width from 30 to 45
        button.setIconSize(QSize(16, 16))
        button.setObjectName(f"{button_type}Button")
        return button

    def _initialize_navigation_buttons(self, landing_page) -> None:
        """Initialize navigation buttons"""
        nav_buttons = {
            landing_page.ui.navigationHomeButton: "home",
            landing_page.ui.navigationDiscoverButton: "discover",
            landing_page.ui.navigationCollectionsButton: "collections",
            landing_page.ui.navigationDownloadsButton: "downloads",
            landing_page.ui.navigationPlayerButton: "player",
            landing_page.ui.navigationNewsButton: "news",
            landing_page.ui.navigationSettingsButton: "settings"
        }
        
        for button, icon_name in nav_buttons.items():
            self.apply_theme_to_button(
                button,
                f"./assets/icons/{icon_name}.svg",
                self.ICON_SIZES['navigation'],
                is_nav_button=True
            )

    def _initialize_control_buttons(self, landing_page) -> None:
        """Initialize control buttons"""
        control_buttons = {
            landing_page.ui.userProfileButton: "profile"
        }
        
        # Handle theme toggle button separately
        self.apply_theme_to_button(
            landing_page.ui.themeToggleButton,
            "./assets/icons/mode-light.svg" if self.is_dark_mode else "./assets/icons/mode-dark.svg"
        )
        
        for button, icon_name in control_buttons.items():
            self.apply_theme_to_button(
                button,
                f"./assets/icons/{icon_name}.svg"
            )
        

    def apply_theme_to_profile_dialog(self, dialog) -> None:
        """Apply theme to profile dialog"""
        # Apply base stylesheet
        dialog.setStyleSheet(self.get_stylesheet())
        
        # Custom button styles
        button_styles = f"""
            #saveButton {{
                background-color: #0078D4;
                color: {self.current_theme.text};
                border-radius: 4px;
                padding: 6px 12px;
            }}
            #saveButton:hover {{
                background-color: #1084D9;
            }}
            #cancelButton {{
                background-color: {self.current_theme.secondary_background};
                color: {self.current_theme.text};
                border-radius: 4px;
                padding: 6px 12px;
            }}
            #cancelButton:hover {{
                background-color: {self.current_theme.hover};
            }}
        """
        dialog.ui.saveButton.setStyleSheet(button_styles)
        dialog.ui.cancelButton.setStyleSheet(button_styles)



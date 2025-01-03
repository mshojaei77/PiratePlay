from pages.base_page import BasePageWidget
from views.home_ui import Ui_HomeWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import requests
from services.tmdb import TMDBService
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import asyncio
from functools import partial
from utils.logger import app_logger
from services.poster_downloader import PosterDownloader

class ClickableMovieContainer(QFrame):
    def __init__(self, parent=None, movie_name=None, click_handler=None):
        super().__init__(parent)
        self.movie_name = movie_name
        self.click_handler = click_handler
        self.setStyleSheet("QFrame:hover { background-color: #34495e; border-radius: 5px; }")
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.click_handler and self.movie_name:
            self.click_handler(self.movie_name)

class HomeWidget(BasePageWidget):
    def __init__(self, app):
        super().__init__(app)
        self.ui = Ui_HomeWidget()
        self.ui.setupUi(self)
        
        # Initialize TMDB service
        self.tmdb = TMDBService()
        
        # Initialize content areas with grid layouts
        self._setup_content_area(self.ui.currentWatchingContent)
        self._setup_content_area(self.ui.trendingMoviesContent)
        self._setup_content_area(self.ui.trendingSeriesContent)
        self._setup_content_area(self.ui.trendingAnimeContent)
        
        # Create cache directory if it doesn't exist
        self.cache_dir = Path("cache/posters")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize thread pool for parallel loading
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        
        # Add PosterDownloader initialization
        self.poster_downloader = PosterDownloader()
        
    def _setup_content_area(self, content_widget, items_count=20):
        # Create horizontal layout for the content
        layout = QHBoxLayout(content_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 5, 10, 5)
        
        for i in range(items_count):
            # Create clickable container widget for poster and title
            container = ClickableMovieContainer(click_handler=lambda name: self.app.show_selected_movie(name))
            container_layout = QVBoxLayout(container)
            container_layout.setSpacing(5)
            container_layout.setContentsMargins(5, 5, 5, 5)
            
            # Create poster label
            poster = QLabel()
            poster.setFixedSize(150, 225)  # 2:3 aspect ratio for posters
            poster.setStyleSheet("background-color: #2c3e50; border-radius: 5px;")
            poster.setAlignment(Qt.AlignCenter)
            
            # Create title label
            title = QLabel("Movie Title")
            title.setAlignment(Qt.AlignCenter)
            title.setWordWrap(True)
            title.setStyleSheet("color: white; font-size: 12px;")
            title.setFixedWidth(150)  # Match poster width
            
            # Add widgets to container
            container_layout.addWidget(poster)
            container_layout.addWidget(title)
            
            # Add container to horizontal layout
            layout.addWidget(container)
        
        # Add stretch at the end to keep items left-aligned
        layout.addStretch()
        
    def on_page_activate(self):
        super().on_page_activate()
        # Load content after page activation
        self._load_trending_movies()

    def _load_poster(self, movie, container):
        movie_title = movie.get('title', 'Unknown')
        # Set the title immediately, regardless of poster status
        title_label = container.findChildren(QLabel)[-1]
        title_label.setText(movie_title)

        def load_and_set_poster():
            try:
                # Get poster data directly as bytes
                poster_data = self.poster_downloader.get_posters_by_name(movie_title)
                
                if not poster_data:
                    app_logger.debug(f"No poster found for movie: {movie_title}")
                    return

                # Create QPixmap from image data
                pixmap = QPixmap()
                if pixmap.loadFromData(poster_data):
                    scaled_pixmap = pixmap.scaled(
                        150, 225,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    
                    if not scaled_pixmap.isNull():
                        poster_label = container.findChild(QLabel)
                        poster_label.setPixmap(scaled_pixmap)
                        app_logger.debug(f"Successfully loaded poster for: {movie_title}")
                    else:
                        raise ValueError("Failed to scale pixmap")
                else:
                    raise ValueError("Failed to load pixmap from image data")
                    
            except Exception as e:
                app_logger.error(f"Error loading poster for {movie_title}: {str(e)}")

        # Submit poster loading task to thread pool
        self.thread_pool.submit(load_and_set_poster)

    def _load_trending_movies(self):
        try:
            trending_movies = self.tmdb.get_trending_movies()
            if "results" not in trending_movies:
                app_logger.error("No results found in trending movies response")
                return

            layout = self.ui.trendingMoviesContent.layout()
            
            for i, movie in enumerate(trending_movies["results"][:20]):
                if i >= layout.count() - 1:
                    break
                    
                container = layout.itemAt(i).widget()
                if container:
                    # Set the movie name for the clickable container
                    container.movie_name = movie.get('title', 'Unknown')
                    self.thread_pool.submit(self._load_poster, movie, container)
                    
        except Exception as e:
            app_logger.error(f"Failed to load trending movies: {str(e)}")

    def on_page_deactivate(self):
        super().on_page_deactivate()
        # Add page-specific cleanup logic here

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
from services.myanimelist import MyAnimeListService
class ClickableMovieContainer(QFrame):
    def __init__(self, parent=None, movie_name=None, movie_id=None, click_handler=None):
        super().__init__(parent)
        self.movie_name = movie_name
        self.movie_id = movie_id
        self.click_handler = click_handler
        self.setStyleSheet("QFrame:hover { background-color: #34495e; border-radius: 5px; }")
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.click_handler:
            self.click_handler(self.movie_name, self.movie_id)

class HomeWidget(BasePageWidget):
    def __init__(self, app):
        super().__init__(app)
        self.ui = Ui_HomeWidget()
        self.ui.setupUi(self)
        
        # Initialize TMDB service
        self.tmdb = TMDBService()
        self.myanimelist = MyAnimeListService()
        
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
            container = ClickableMovieContainer(
                click_handler=lambda name, id: self.app.show_selected_movie(name, id)  # Updated lambda to accept both parameters
            )
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
        self._load_trending_series()
        self._load_trending_anime()

    def _load_poster(self, movie, container):
        movie_title = movie.get('title') or movie.get('name', 'Unknown')
        movie_id = movie.get('id')
        
        # Set the title and ID immediately
        title_label = container.findChildren(QLabel)[-1]
        title_label.setText(movie_title)
        container.movie_id = movie_id

        def load_and_set_poster():
            try:
                # Get poster data using both name and ID
                poster_data = self.poster_downloader.get_posters_by_name(movie_title)
                
                if not poster_data:
                    app_logger.debug(f"No poster found for movie: {movie_title} (ID: {movie_id})")
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
                        app_logger.debug(f"Successfully loaded poster for: {movie_title} (ID: {movie_id})")
                    else:
                        raise ValueError("Failed to scale pixmap")
                else:
                    raise ValueError("Failed to load pixmap from image data")
                    
            except Exception as e:
                app_logger.error(f"Error loading poster for {movie_title} (ID: {movie_id}): {str(e)}")

        # Submit poster loading task to thread pool
        self.thread_pool.submit(load_and_set_poster)
        
    def _load_tv_poster(self, tv, container):
        tv_title = tv.get('name', 'Unknown')
        tv_id = tv.get('id')
        
        # Set the title and ID immediately
        title_label = container.findChildren(QLabel)[-1]
        title_label.setText(tv_title)
        container.movie_id = tv_id

        def load_and_set_poster():
            try:
                poster_data = self.poster_downloader.get_tv_posters_by_name(tv_title)
                
                if not poster_data:
                    app_logger.debug(f"No poster found for TV show: {tv_title} (ID: {tv_id})")
                    return

                pixmap = QPixmap()
                if pixmap.loadFromData(poster_data):
                    # Get the poster label's size
                    poster_label = container.findChild(QLabel)
                    label_size = poster_label.size()
                    
                    # Scale the pixmap to fill the label while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(
                        label_size.width(),
                        label_size.height(),
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation
                    )
                    
                    # If the scaled image is larger than the label, crop it from the center
                    if scaled_pixmap.width() > label_size.width() or scaled_pixmap.height() > label_size.height():
                        x = (scaled_pixmap.width() - label_size.width()) // 2
                        y = (scaled_pixmap.height() - label_size.height()) // 2
                        scaled_pixmap = scaled_pixmap.copy(
                            x, y, label_size.width(), label_size.height()
                        )
                    
                    if not scaled_pixmap.isNull():
                        poster_label.setPixmap(scaled_pixmap)
                        app_logger.debug(f"Successfully loaded poster for TV show: {tv_title} (ID: {tv_id})")
                    else:
                        raise ValueError("Failed to scale pixmap")
                else:
                    raise ValueError("Failed to load pixmap from image data")
                    
            except Exception as e:
                app_logger.error(f"Error loading poster for TV show {tv_title} (ID: {tv_id}): {str(e)}")

        # Submit poster loading task to thread pool
        self.thread_pool.submit(load_and_set_poster)

    def _load_anime_poster(self, anime, container):
        anime_title = anime.get('name', 'Unknown')
        anime_id = anime.get('id')
        
        # Set the title and ID immediately
        title_label = container.findChildren(QLabel)[-1]
        title_label.setText(anime_title)
        container.movie_id = anime_id

        def load_and_set_poster():
            try:
                # First try to get poster from MyAnimeList via poster downloader
                poster_data = self.poster_downloader.get_anime_poster_by_name(anime_title, anime_id)
                
                if not poster_data:
                    app_logger.debug(f"No MAL poster found for anime: {anime_title}, falling back to TV poster")
                    # Fall back to TV poster method
                    return self._load_tv_poster(anime, container)

                pixmap = QPixmap()
                if pixmap.loadFromData(poster_data):
                    # Get the poster label's size
                    poster_label = container.findChild(QLabel)
                    label_size = poster_label.size()
                    
                    # Scale the pixmap to fill the label while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(
                        label_size.width(),
                        label_size.height(),
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation
                    )
                    
                    # If the scaled image is larger than the label, crop it from the center
                    if scaled_pixmap.width() > label_size.width() or scaled_pixmap.height() > label_size.height():
                        x = (scaled_pixmap.width() - label_size.width()) // 2
                        y = (scaled_pixmap.height() - label_size.height()) // 2
                        scaled_pixmap = scaled_pixmap.copy(
                            x, y, label_size.width(), label_size.height()
                        )
                    
                    if not scaled_pixmap.isNull():
                        poster_label.setPixmap(scaled_pixmap)
                        app_logger.debug(f"Successfully loaded MAL poster for: {anime_title} (ID: {anime_id})")
                    else:
                        raise ValueError("Failed to scale pixmap")
                else:
                    raise ValueError("Failed to load pixmap from image data")
                    
            except Exception as e:
                app_logger.error(f"Error loading MAL poster for {anime_title} (ID: {anime_id}): {str(e)}")
                # Fall back to TV poster method
                return self._load_tv_poster(anime, container)

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
                    # Set both movie name and ID for the clickable container
                    container.movie_name = movie.get('title', 'Unknown')
                    container.movie_id = movie.get('id')
                    self.thread_pool.submit(self._load_poster, movie, container)
                    
        except Exception as e:
            app_logger.error(f"Failed to load trending movies: {str(e)}")

    def _load_trending_series(self):
        try:
            trending_series = self.tmdb.get_trending_tv()
            if "results" not in trending_series:
                app_logger.error("No results found in trending series response")
                return

            layout = self.ui.trendingSeriesContent.layout()
            
            for i, series in enumerate(trending_series["results"][:20]):
                if i >= layout.count() - 1:
                    break
                    
                container = layout.itemAt(i).widget()
                if container:
                    # Set both series name and ID for the clickable container
                    container.movie_name = series.get('name', 'Unknown')
                    container.movie_id = series.get('id')
                    self.thread_pool.submit(self._load_tv_poster, series, container)
                    
        except Exception as e:
            app_logger.error(f"Failed to load trending series: {str(e)}")

    def _load_trending_anime(self):
        try:
            trending_anime = self.myanimelist.get_trending_anime()
            if "results" not in trending_anime:
                app_logger.error("No results found in trending anime response")
                return

            layout = self.ui.trendingAnimeContent.layout()
            
            for i, anime in enumerate(trending_anime["results"][:20]):
                if i >= layout.count() - 1:
                    break
                    
                container = layout.itemAt(i).widget()
                if container:
                    # Set both anime name and ID for the clickable container
                    
                    container.movie_name = anime.get('name', 'Unknown')
                    container.movie_id = anime.get('id')
                    print(anime.get('id'))
                    self._load_anime_poster(anime, container)
                    
        except Exception as e:
            app_logger.error(f"Failed to load trending anime: {str(e)}")

    def on_page_deactivate(self):
        super().on_page_deactivate()
        # Add page-specific cleanup logic here

import requests
from bs4 import BeautifulSoup
from typing import List
import re
from urllib.parse import quote
import logging
import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os
from pathlib import Path

app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.DEBUG)

class PosterDownloader:

    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Add timeout to session defaults
        self.session.timeout = 5
        # Add response caching
        self._cache = {}

        # Add API keys as class attributes
        self.FANART_API_KEY = "394b6ff839ec90283384715051d85f54"
        self.TMDB_API_KEY = "917cce472ff1093d25cd89d8c007aacd"
        self.TMDB_BASE_URL = "https://api.themoviedb.org/3/"

        self._shutdown_event = threading.Event()

        # Add cache directory for images
        self.cache_dir = Path("cache/posters")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_posters_by_name(self, movie_name: str) -> bytes:
        """Get movie poster image data, trying all sources concurrently until first success"""
        # Create cache filename
        cache_file = self.cache_dir / f"{movie_name.replace(' ', '_')}.jpg"

        # Check file cache first
        if cache_file.exists():
            return cache_file.read_bytes()

        # Check memory cache
        cache_key = f"poster_{movie_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        movie_name_encoded = quote(movie_name)
        movie_name_rt = movie_name.replace(" ", "_")

        # Expanded sources list to include all methods
        sources = [
            (self._get_tmdb_api_poster_url, movie_name),
            (self._get_fanart_poster_url, movie_name),
            (self._get_yts_poster_url, movie_name),
            (self._get_rt_poster, movie_name_rt),
            (self._get_tmdb_poster, movie_name_encoded),
            (self._get_imdb_poster, movie_name_encoded),
        ]

        poster_data = None
        with ThreadPoolExecutor(max_workers=len(sources)) as executor:
            future_to_source = {
                executor.submit(source, name): source.__name__ 
                for source, name in sources
            }

            try:
                for future in as_completed(future_to_source):
                    source_name = future_to_source[future]
                    try:
                        poster_url = future.result()
                        if poster_url and self._is_valid_image_url(poster_url):
                            # Download the image
                            response = self.session.get(poster_url, stream=True)
                            if response.ok:
                                poster_data = response.content
                                # Save to file cache
                                cache_file.write_bytes(poster_data)
                                # Save to memory cache
                                self._cache[cache_key] = poster_data
                                self._shutdown_event.set()
                                break
                    except Exception as e:
                        app_logger.debug(f"Error getting poster from {source_name}: {str(e)}")

            finally:
                # Cancel remaining futures
                for future in future_to_source:
                    if not future.done():
                        future.cancel()

        return poster_data if poster_data else bytes()

    def _is_valid_image_url(self, url: str) -> bool:
        """Validate image URL format without making a request"""
        image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        return any(url.lower().endswith(ext) for ext in image_extensions)

    def _get_imdb_poster(self, movie_name_encoded: str) -> str:
        """Get poster from IMDB"""
        imdb_search_url = f"https://www.imdb.com/find?q={movie_name_encoded}"
        response = self.session.get(imdb_search_url)
        if not response.ok:
            return ""
            
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', class_='ipc-metadata-list-summary-item__t')
        if not first_result:
            return ""

        # Extract movie ID from href to construct direct image URL
        movie_id_match = re.search(r'/title/(tt\d+)/', first_result['href'])
        if movie_id_match:
            # Construct direct poster URL using movie ID
            return f"https://m.media-amazon.com/images/M/{movie_id_match.group(1)}@._V1_SX300.jpg"
        return ""

    def _get_rt_poster(self, movie_name_underscore: str) -> str:
        """Get poster from Rotten Tomatoes using underscore-separated name"""
        rt_url = f"https://www.rottentomatoes.com/m/{movie_name_underscore}"
        response = self.session.get(rt_url)
        if not response.ok:
            return ""
            
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_img = soup.find('meta', {'property': 'og:image'})
        if meta_img and meta_img.get('content'):
            content = meta_img['content']
            if 'flixster.com' in content:
                base_url = content.split('/v2/')[1] if '/v2/' in content else content
                return f"https://resizing.flixster.com/{base_url}"
        return ""

    def _get_tmdb_poster(self, movie_name_encoded: str) -> str:
        """Get poster from TheMovieDB"""
        tmdb_url = f"https://www.themoviedb.org/search?query={movie_name_encoded}"
        response = self.session.get(tmdb_url)
        if not response.ok:
            return ""
            
        soup = BeautifulSoup(response.text, 'html.parser')
        poster = soup.find('img', class_='poster')
        if poster and poster.get('src'):
            return f"https://image.tmdb.org{poster['src']}"
        return ""

    def get_fanart_posters(self, movie_id: str) -> List[str]:
        """Get movie posters from Fanart.tv API for a given movie ID"""
        BASE_URL = "http://webservice.fanart.tv/v3/"
        API_KEY = "394b6ff839ec90283384715051d85f54"

        session = requests.Session()
        session.params = {'api_key': API_KEY}

        url = urljoin(BASE_URL, f"movies/{movie_id}")
        try:
            response = session.get(url)
            response.raise_for_status()
            data = response.json()

            if not data or 'movieposter' not in data:
                return []
                
            posters = data['movieposter']
            if not posters:
                return []
                
            # Sort posters by likes and language preference
            posters.sort(key=lambda x: (x.get('lang') == 'en', int(x.get('likes', 0))), reverse=True)
            
            return [poster['url'] for poster in posters]

        except requests.exceptions.RequestException as e:
            app_logger.debug(f"Error getting posters for movie {movie_id}: {str(e)}")
            return []

    def get_yts_poster(self, movie_name: str) -> dict | None:
        """
        Fetch a movie's poster URLs from YTS by title.
        
        Args:
            movie_name: Name of the movie to search for
        
        Returns:
            dict | None: Dictionary containing poster URLs or None if not found
            {
                'small': small_cover_image,
                'medium': medium_cover_image,
                'large': large_cover_image
            }
        """
        BASE_URL = "https://yts.mx/api/v2"
        
        try:
            # Make request to YTS API
            response = requests.get(
                f"{BASE_URL}/list_movies.json",
                params={"query_term": movie_name, "limit": 1}
            )
            response.raise_for_status()
            data = response.json()
            
            # Check if movie was found and return poster URLs
            if (data["status"] == "ok" and 
                "data" in data and 
                "movies" in data["data"] and 
                data["data"]["movies"]):
                
                movie = data["data"]["movies"][0]
                return {
                    "small": movie["small_cover_image"],
                    "medium": movie["medium_cover_image"],
                    "large": movie["large_cover_image"]
                }
                
        except Exception as e:
            print(f"Error fetching poster for {movie_name}: {str(e)}")
        
        return None

    def get_tmdb_api_poster(self, movie_name: str, api_key: str = "917cce472ff1093d25cd89d8c007aacd") -> str:
        """
        Get movie poster URL by movie name using TMDB API
        
        Args:
            movie_name (str): Name of the movie to search for
            api_key (str): TMDB API key (optional)
            
        Returns:
            str: URL of the movie poster, or empty string if not found
        """
        BASE_URL = "https://api.themoviedb.org/3/"
        POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
        
        # Search for the movie
        search_url = f"{BASE_URL}search/movie"
        params = {
            "api_key": api_key,
            "query": movie_name
        }
        
        try:
            # Make the search request
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            search_results = response.json()
            
            # Get poster path from first result
            if "results" in search_results and search_results["results"]:
                poster_path = search_results["results"][0].get("poster_path")
                if poster_path:
                    return f"{POSTER_BASE_URL}{poster_path}"
        except requests.exceptions.RequestException as e:
            print(f"Error fetching poster: {str(e)}")
        
        return ""

    def _get_yts_poster_url(self, movie_name: str) -> str:
        """Helper method to get single URL from YTS"""
        result = self.get_yts_poster(movie_name)
        if result and result.get("large"):
            return result["large"]
        return ""

    def _get_tmdb_api_poster_url(self, movie_name: str) -> str:
        """Helper method to get single URL from TMDB API"""
        if self._should_stop():
            return ""
        return self.get_tmdb_api_poster(movie_name, self.TMDB_API_KEY)

    def _get_tmdb_movie_id(self, movie_name: str) -> str:
        """Get TMDB movie ID for Fanart.tv API"""
        search_url = f"{self.TMDB_BASE_URL}search/movie"
        params = {
            "api_key": self.TMDB_API_KEY,
            "query": movie_name
        }
        
        try:
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            search_results = response.json()
            
            if "results" in search_results and search_results["results"]:
                return str(search_results["results"][0]["id"])
        except Exception as e:
            app_logger.debug(f"Error getting TMDB ID for {movie_name}: {str(e)}")
        
        return ""

    def _get_fanart_poster_url(self, movie_name: str) -> str:
        """Helper method to get single URL from Fanart.tv"""
        if self._should_stop():
            return ""
        movie_id = self._get_tmdb_movie_id(movie_name)
        if not movie_id:
            return ""
        posters = self.get_fanart_posters(movie_id)
        return posters[0] if posters else ""

    def _should_stop(self) -> bool:
        return self._shutdown_event.is_set()

if __name__ == "__main__":
    # Example usage of the PosterDownloader
    scraper = PosterDownloader()
    
    # Test with a popular movie
    movie_name = "The Shawshank Redemption"
    poster_data = scraper.get_posters_by_name(movie_name)
    print(poster_data)

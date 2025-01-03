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
from services.tmdb import TMDBService
from services.myanimelist import MyAnimeListService

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

        self.tmdb_service = TMDBService(self.TMDB_API_KEY)
        self.myanimelist = MyAnimeListService()

    def get_posters_by_name(self, movie_name: str) -> bytes:
        """Get movie poster image data, trying all sources concurrently until first success"""
        # Get movie ID from TMDB first
        movie_id = self.tmdb_service.get_movie_id_by_name(movie_name)
        
        # Create cache key using both name and ID
        cache_key = f"poster_{movie_name}_{movie_id}" if movie_id else f"poster_{movie_name}"
        
        # Check memory cache with new key
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Extract year and clean movie name

        clean_name = movie_name

        # Create cache filename with sanitized name and movie ID
        cache_filename = clean_name.lower()  # Convert to lowercase
        cache_filename = re.sub(r'[^\w\-_\. ]', '', cache_filename)  # Remove special chars
        cache_filename = re.sub(r'\s+', '_', cache_filename)  # Replace spaces with underscore
        cache_filename = re.sub(r'_{2,}', '_', cache_filename)  # Remove multiple underscores
        cache_filename = cache_filename.strip('_')  # Remove leading/trailing underscores
        
        # Add movie ID to filename if available
        if movie_id:
            cache_filename = f"{cache_filename}_{movie_id}"
        
        cache_file = self.cache_dir / f"{cache_filename}.jpg"

        # Check file cache first
        if cache_file.exists():
            return cache_file.read_bytes()

        movie_name_encoded = quote(movie_name)
        movie_name_rt = movie_name.replace(" ", "_")

        # Pass both name and ID to source methods
        sources = [
            (self._get_tmdb_api_poster_url, (movie_name, movie_id)),
            (self._get_fanart_poster_url, (movie_name, movie_id)),
            (self._get_yts_poster_url, (movie_name, movie_id)),
            (self._get_rt_poster, movie_name_rt),  # RT uses name-based URLs
            (self._get_tmdb_poster, movie_name_encoded),  # Web scraping still uses name
            (self._get_imdb_poster, movie_name_encoded),  # Web scraping still uses name
        ]

        poster_data = None
        # Create a new executor for each call to avoid shutdown issues
        with ThreadPoolExecutor(max_workers=len(sources)) as executor:
            futures = []
            for source, params in sources:
                if not self._shutdown_event.is_set():
                    if isinstance(params, tuple):
                        futures.append(executor.submit(source, *params))
                    else:
                        futures.append(executor.submit(source, params))

            try:
                for future in as_completed(futures):
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
                                break
                    except Exception as e:
                        app_logger.debug(f"Error getting poster: {str(e)}")
                        continue

            finally:
                # Cancel any remaining futures
                for future in futures:
                    if not future.done():
                        future.cancel()

        return poster_data if poster_data else bytes()
    
    def get_tv_posters_by_name(self, tv_name: str) -> bytes:
        """Get TV show poster image data, trying all sources concurrently until first success"""
        # Get TV show ID from TMDB first
        tv_id = self.tmdb_service.get_tv_id_by_name(tv_name)

        # Create cache key using both name and ID
        cache_key = f"tv_poster_{tv_name}_{tv_id}" if tv_id else f"tv_poster_{tv_name}"
        
        # Check memory cache with new key
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Create cache filename with sanitized name and TV ID
        cache_filename = self._sanitize_filename(tv_name, tv_id)
        cache_file = self.cache_dir / f"{cache_filename}.jpg"

        # Check file cache first
        if cache_file.exists():
            return cache_file.read_bytes()

        tv_name_encoded = quote(tv_name)
        tv_name_rt = tv_name.replace(" ", "_")

        # Define sources to try (expanded with more TV-specific endpoints)
        sources = [
            (self._get_tmdb_tv_api_poster_url, (tv_name, tv_id)),  # Direct TMDB API call
            (self._get_fanart_tv_poster_url, (tv_name, tv_id)),    # Fanart.tv TV endpoint
            (self._get_rt_tv_poster, tv_name_rt),                  # RT TV endpoint
            (self._get_tvdb_poster_url, tv_name_encoded),          # TVDB fallback
            (self._get_imdb_tv_poster, tv_name_encoded),          # IMDB TV fallback
            (self._get_tmdb_poster, tv_name_encoded),             # Web scraping fallback
        ]

        poster_data = self._try_sources_concurrently(sources, cache_file, cache_key)
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

    def _get_yts_poster_url(self, movie_name: str, movie_id: int = None) -> str:
        """Helper method to get single URL from YTS"""
        # YTS API doesn't support TMDB IDs, so we still use movie name
        result = self.get_yts_poster(movie_name)
        if result and result.get("large"):
            return result["large"]
        return ""

    def _get_tmdb_api_poster_url(self, movie_name: str, movie_id: int = None) -> str:
        """Helper method to get single URL from TMDB API"""
        if self._should_stop():
            return ""
        if movie_id:
            # Use movie_id directly if available
            movie_details = self.tmdb_service.get_movie_details(movie_id)
            if movie_details and "poster_path" in movie_details:
                return f"{self.tmdb_service.POSTER_BASE_URL}{movie_details['poster_path']}"
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

    def _get_fanart_poster_url(self, movie_name: str, movie_id: int = None) -> str:
        """Helper method to get single URL from Fanart.tv"""
        if self._should_stop():
            return ""
        tmdb_id = str(movie_id) if movie_id else self._get_tmdb_movie_id(movie_name)
        if not tmdb_id:
            return ""
        posters = self.get_fanart_posters(tmdb_id)
        return posters[0] if posters else ""

    def _should_stop(self) -> bool:
        return self._shutdown_event.is_set()

    def _get_fanart_tv_poster_url(self, tv_name: str, tv_id: int = None) -> str:
        """Get TV show poster from Fanart.tv"""
        if self._should_stop():
            return ""
        if not tv_id:
            return ""
        
        BASE_URL = "http://webservice.fanart.tv/v3/"
        url = f"{BASE_URL}tv/{tv_id}"
        
        try:
            response = self.session.get(
                url,
                params={'api_key': self.FANART_API_KEY}
            )
            response.raise_for_status()
            data = response.json()
            
            if 'tvposter' in data and data['tvposter']:
                # Sort by likes and language preference
                posters = sorted(
                    data['tvposter'],
                    key=lambda x: (x.get('lang') == 'en', int(x.get('likes', 0))),
                    reverse=True
                )
                return posters[0]['url']
        except Exception as e:
            app_logger.debug(f"Error getting Fanart.tv TV poster: {str(e)}")
        
        return ""

    def _get_rt_tv_poster(self, tv_name_underscore: str) -> str:
        """Get TV show poster from Rotten Tomatoes"""
        rt_url = f"https://www.rottentomatoes.com/tv/{tv_name_underscore}"
        try:
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
        except Exception as e:
            app_logger.debug(f"Error getting RT TV poster: {str(e)}")
        
        return ""

    def _get_tmdb_tv_api_poster_url(self, tv_name: str, tv_id: int = None) -> str:
        """Get TV show poster directly from TMDB API"""
        if self._should_stop():
            return ""
        try:
            if tv_id:
                # Use TV ID directly if available
                details = self.tmdb_service.get_tv_details(tv_id)
                if details and "poster_path" in details:
                    return f"{self.tmdb_service.POSTER_BASE_URL}{details['poster_path']}"
            
            # Fallback to search if no ID or no results
            search_url = f"{self.TMDB_BASE_URL}search/tv"
            response = self.session.get(
                search_url,
                params={
                    "api_key": self.TMDB_API_KEY,
                    "query": tv_name
                }
            )
            data = response.json()
            if data.get("results"):
                poster_path = data["results"][0].get("poster_path")
                if poster_path:
                    return f"{self.tmdb_service.POSTER_BASE_URL}{poster_path}"
        except Exception as e:
            app_logger.debug(f"Error getting TMDB TV poster: {str(e)}")
        return ""

    def _get_tvdb_poster_url(self, tv_name: str) -> str:
        """Get TV show poster from TVDB"""
        try:
            search_url = f"https://thetvdb.com/search?query={tv_name}"
            response = self.session.get(search_url)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                poster = soup.select_one('.thumbnail img')
                if poster and poster.get('src'):
                    return urljoin("https://thetvdb.com", poster['src'])
        except Exception as e:
            app_logger.debug(f"Error getting TVDB poster: {str(e)}")
        return ""

    def _get_imdb_tv_poster(self, tv_name: str) -> str:
        """Get TV show poster from IMDB"""
        try:
            # Add "TV series" to search query to prioritize TV results
            imdb_search_url = f"https://www.imdb.com/find?q={tv_name}+TV+series"
            response = self.session.get(imdb_search_url)
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Look specifically for TV series results
                first_result = soup.find('a', class_='ipc-metadata-list-summary-item__t', 
                                       href=lambda x: x and '/title/tt' in x)
                if first_result:
                    show_id_match = re.search(r'/title/(tt\d+)/', first_result['href'])
                    if show_id_match:
                        return f"https://m.media-amazon.com/images/M/{show_id_match.group(1)}@._V1_SX300.jpg"
        except Exception as e:
            app_logger.debug(f"Error getting IMDB TV poster: {str(e)}")
        return ""

    def _sanitize_filename(self, name: str, id: int = None) -> str:
        """Helper method to create sanitized cache filenames"""
        filename = name.lower()
        filename = re.sub(r'[^\w\-_\. ]', '', filename)
        filename = re.sub(r'\s+', '_', filename)
        filename = re.sub(r'_{2,}', '_', filename)
        filename = filename.strip('_')
        return f"{filename}_{id}" if id else filename

    def _try_sources_concurrently(self, sources, cache_file, cache_key):
        """Helper method to try multiple sources concurrently"""
        poster_data = None
        with ThreadPoolExecutor(max_workers=len(sources)) as executor:
            futures = []
            for source, params in sources:
                if not self._shutdown_event.is_set():
                    if isinstance(params, tuple):
                        futures.append(executor.submit(source, *params))
                    else:
                        futures.append(executor.submit(source, params))

            try:
                for future in as_completed(futures):
                    try:
                        poster_url = future.result()
                        if poster_url and self._is_valid_image_url(poster_url):
                            response = self.session.get(poster_url, stream=True)
                            if response.ok:
                                poster_data = response.content
                                cache_file.write_bytes(poster_data)
                                self._cache[cache_key] = poster_data
                                break
                    except Exception as e:
                        app_logger.debug(f"Error getting TV poster: {str(e)}")
                        continue
            finally:
                for future in futures:
                    if not future.done():
                        future.cancel()
        return poster_data

    def get_anime_poster_by_name(self, anime_name: str, anime_id: int = None) -> bytes:
        """Get anime poster image data with caching"""
        # Create cache key using both name and ID
        cache_key = f"anime_poster_{anime_name}_{anime_id}" if anime_id else f"anime_poster_{anime_name}"
        
        # Check memory cache
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Create cache filename
        cache_filename = self._sanitize_filename(anime_name, anime_id)
        cache_file = self.cache_dir / f"{cache_filename}.jpg"

        # Check file cache
        if cache_file.exists():
            return cache_file.read_bytes()

        # Get poster URL from MAL
        poster_url = self.myanimelist.get_anime_poster_by_id(anime_id) if anime_id else ""
        
        if not poster_url:
            return bytes()

        try:
            # Download the image
            response = self.session.get(poster_url, stream=True)
            if response.ok:
                poster_data = response.content
                # Save to file cache
                cache_file.write_bytes(poster_data)
                # Save to memory cache
                self._cache[cache_key] = poster_data
                return poster_data
        except Exception as e:
            app_logger.debug(f"Error downloading anime poster: {str(e)}")
        
        return bytes()

if __name__ == "__main__":
    # Example usage of the PosterDownloader
    scraper = PosterDownloader()
    
    # Test with a popular movie
    movie_name = "The Shawshank Redemption"
    poster_data = scraper.get_posters_by_name(movie_name)
    if poster_data:
        print(f"Successfully retrieved movie poster for '{movie_name}'")
        # Save to test file
        with open("test_movie_poster.jpg", "wb") as f:
            f.write(poster_data)
    
    # Test with a popular TV show
    tv_name = "Breaking Bad"
    tv_poster_data = scraper.get_tv_posters_by_name(tv_name)
    if tv_poster_data:
        print(f"Successfully retrieved TV poster for '{tv_name}'")
        # Save to test file
        with open("test_tv_poster.jpg", "wb") as f:
            f.write(tv_poster_data)

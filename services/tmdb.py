from typing import Optional, Dict, Any, List
import requests
import time
from urllib.parse import urljoin
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3/"
    POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
    
    def __init__(self, api_key: str = "917cce472ff1093d25cd89d8c007aacd"):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.params = {'api_key': self.api_key}
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make API request with rate limiting and error handling"""
        url = urljoin(self.BASE_URL, endpoint)
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            time.sleep(0.25)  # Rate limiting
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {str(e)}")
            return {}

    @lru_cache(maxsize=128)
    def get_trending_movies(self, page: int = 1) -> List[Dict]:
        """Get trending movies for home page movies section"""
        return self._make_request("trending/movie/week", params={"page": str(page)})

    @lru_cache(maxsize=128)
    def get_trending_tv(self, page: int = 1) -> List[Dict]:
        """Get trending TV shows for home page series section"""
        return self._make_request("trending/tv/week", params={"page": str(page)})

    @lru_cache(maxsize=128)
    def get_new_episodes(self, show_ids: List[int]) -> List[Dict]:
        """Get new episodes for shows user is watching"""
        episodes = []
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.get_tv_details, show_id): show_id for show_id in show_ids}
            for future in as_completed(futures):
                show_details = future.result()
                if show_details and 'last_episode_to_air' in show_details:
                    episodes.append(show_details['last_episode_to_air'])
        return episodes
        
    @lru_cache(maxsize=128)
    def search_multi(self, query: str) -> List[Dict]:
        """Search for movies, TV shows and people"""
        return self._make_request("search/multi", params={"query": query})
        
    @lru_cache(maxsize=128)
    def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed movie information"""
        return self._make_request(f"movie/{movie_id}", 
                                params={"append_to_response": "videos,credits,similar,recommendations"})
        
    @lru_cache(maxsize=128)
    def get_tv_details(self, tv_id: int) -> Dict:
        """Get detailed TV show information"""
        return self._make_request(f"tv/{tv_id}",
                                params={"append_to_response": "videos,credits,similar,recommendations,season/1"})
                                
    @lru_cache(maxsize=128)
    def get_poster_url(self, poster_path: str) -> str:
        """Get full poster image URL"""
        if not poster_path:
            return ""
        return urljoin(self.POSTER_BASE_URL, poster_path)

    @lru_cache(maxsize=128)
    def get_movie_poster_by_name(self, movie_name: str) -> tuple[str, int]:
        """Get movie poster URL and ID by movie name"""
        search_results = self._make_request("search/movie", params={"query": movie_name})
        if search_results and "results" in search_results and search_results["results"]:
            movie = search_results["results"][0]  # Get first match
            movie_id = movie.get("id", 0)
            poster_path = movie.get("poster_path", "")
            return (self.get_poster_url(poster_path), movie_id)
        return ("", 0)

    @lru_cache(maxsize=128)
    def get_movie_poster_by_id(self, movie_id: int) -> str:
        """Get movie poster URL directly by ID"""
        movie_details = self.get_movie_details(movie_id)
        if movie_details and "poster_path" in movie_details:
            return self.get_poster_url(movie_details["poster_path"])
        return ""

    @lru_cache(maxsize=128)
    def get_movie_name_by_id(self, movie_id: int) -> str:
        """Get movie name by movie ID"""
        movie_details = self._make_request(f"movie/{movie_id}")
        if movie_details and "title" in movie_details:
            return movie_details["title"]
        return ""

    @lru_cache(maxsize=128)
    def get_movie_id_by_name(self, movie_name: str) -> int:
        """Get movie ID by movie name"""
        search_results = self._make_request("search/movie", params={"query": movie_name})
        if search_results and "results" in search_results and search_results["results"]:
            movie = search_results["results"][0]  # Get first match
            if "id" in movie:
                return movie["id"]
        return 0

    @lru_cache(maxsize=128)
    def get_tv_id_by_name(self, tv_name: str) -> int:
        """Get TV show ID by show name"""
        search_results = self._make_request("search/tv", params={"query": tv_name})
        if search_results and "results" in search_results and search_results["results"]:
            show = search_results["results"][0]  # Get first match
            if "id" in show:
                return show["id"]
        return 0

    @lru_cache(maxsize=128)
    def get_tv_poster_by_id(self, tv_id: int) -> str:
        """Get TV show poster URL directly by ID"""
        tv_details = self.get_tv_details(tv_id)
        if tv_details and "poster_path" in tv_details:
            return self.get_poster_url(tv_details["poster_path"])
        return ""

# Usage example
if __name__ == "__main__":
    # Initialize service
    tmdb = TMDBService()
    
    # Test trending movies
    print("\n=== Trending Movies ===")
    trending_movies = tmdb.get_trending_movies()
    if "results" in trending_movies:
        for movie in trending_movies["results"]:  # Removed [:3]
            print(f"Movie: {movie.get('title')} ({movie.get('release_date', 'N/A')})")
    
    # Test trending TV shows
    print("\n=== Trending TV Shows ===")
    trending_tv = tmdb.get_trending_tv()
    if "results" in trending_tv:
        for show in trending_tv["results"]:  # Removed [:3]
            print(f"Show: {show.get('name')} ({show.get('first_air_date', 'N/A')})")
    
    # Test search
    print("\n=== Search Results ===")
    search_query = "Inception"
    search_results = tmdb.search_multi(search_query)
    if "results" in search_results:
        for result in search_results["results"]:  # Removed [:3]
            media_type = result.get('media_type')
            title = result.get('title') if media_type == 'movie' else result.get('name')
            print(f"{media_type.title()}: {title}")
    
    # Test movie details
    print("\n=== Movie Details ===")
    inception_id = 27205  # Inception movie ID
    movie_details = tmdb.get_movie_details(inception_id)
    print(f"Title: {movie_details.get('title')}")
    print(f"Runtime: {movie_details.get('runtime')} minutes")
    print(f"Rating: {movie_details.get('vote_average')}")
    
    # Test TV show details
    print("\n=== TV Show Details ===")
    breaking_bad_id = 1396  # Breaking Bad show ID
    tv_details = tmdb.get_tv_details(breaking_bad_id)
    print(f"Title: {tv_details.get('name')}")
    print(f"Seasons: {tv_details.get('number_of_seasons')}")
    print(f"Episodes: {tv_details.get('number_of_episodes')}")
    
    # Test poster URLs
    print("\n=== Poster URLs ===")
    movie_name = "The Matrix"
    poster_url = tmdb.get_movie_poster_by_name(movie_name)
    print(f"Poster URL for {movie_name}: {poster_url}")
    
    # Test TV show ID and poster lookup
    print("\n=== TV Show ID and Poster Lookup ===")
    show_name = "Breaking Bad"
    show_id = tmdb.get_tv_id_by_name(show_name)
    print(f"TV Show ID for {show_name}: {show_id}")
    
    poster_url = tmdb.get_tv_poster_by_id(show_id)
    print(f"Poster URL for {show_name}: {poster_url}")

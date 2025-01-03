from dataclasses import dataclass
from typing import List, Optional
import requests
from datetime import datetime

@dataclass
class Torrent:
    url: str
    hash: str
    quality: str
    type: str
    is_repack: str
    video_codec: str
    bit_depth: str
    audio_channels: str
    seeds: int
    peers: int
    size: str
    size_bytes: int
    date_uploaded: str
    date_uploaded_unix: int

@dataclass
class Movie:
    id: int
    url: str
    imdb_code: str
    title: str
    title_english: str
    title_long: str
    slug: str
    year: int
    rating: float
    runtime: int
    genres: List[str]
    summary: str
    description_full: str
    synopsis: str
    yt_trailer_code: str
    language: str
    mpa_rating: str
    background_image: str
    background_image_original: str
    small_cover_image: str
    medium_cover_image: str
    large_cover_image: str
    state: str
    torrents: List[Torrent]
    date_uploaded: str
    date_uploaded_unix: int

class YTSService:
    BASE_URL = "https://yts.mx/api/v2"
    
    def __init__(self):
        self._session = requests.Session()
        self._params = {
            "limit": 20,
            "page": 1,
            "quality": None,
            "minimum_rating": 0,
            "query_term": None,
            "genre": None,
            "sort_by": "date_added",
            "order_by": "desc",
            "with_rt_ratings": False
        }

    def set_params(self, **kwargs):
        """Set search parameters"""
        for key, value in kwargs.items():
            if key in self._params:
                self._params[key] = value

    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """Make API request and handle response"""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self._session.get(url, params=params or self._params)
        response.raise_for_status()
        return response.json()

    def list_movies(self) -> List[Movie]:
        """Get list of movies based on current parameters"""
        response = self._make_request("list_movies.json")
        if response["status"] != "ok":
            raise Exception(response["status_message"])
        
        movies_data = response["data"]["movies"]
        return [Movie(**movie_data) for movie_data in movies_data]

    def get_movie_details(self, movie_id: int) -> Movie:
        """Get detailed information about a specific movie"""
        response = self._make_request("movie_details.json", {"movie_id": movie_id})
        if response["status"] != "ok":
            raise Exception(response["status_message"])
        
        return Movie(**response["data"]["movie"])

    def search_movies(self, query: str) -> List[Movie]:
        """Search movies by title"""
        self._params["query_term"] = query
        return self.list_movies()

    def filter_by_genre(self, genre: str) -> List[Movie]:
        """Filter movies by genre"""
        self._params["genre"] = genre
        return self.list_movies()

    def filter_by_quality(self, quality: str) -> List[Movie]:
        """Filter movies by quality (720p, 1080p, 2160p)"""
        self._params["quality"] = quality
        return self.list_movies()

    def filter_by_rating(self, minimum_rating: float) -> List[Movie]:
        """Filter movies by minimum rating"""
        self._params["minimum_rating"] = minimum_rating
        return self.list_movies()

    def sort_movies(self, sort_by: str, order_by: str = "desc") -> List[Movie]:
        """
        Sort movies by specified criteria
        sort_by options: title, year, rating, peers, seeds, download_count, like_count, date_added
        order_by options: desc, asc
        """
        self._params["sort_by"] = sort_by
        self._params["order_by"] = order_by
        return self.list_movies()

    def set_page(self, page: int, limit: int = 20) -> List[Movie]:
        """Set page number and results per page"""
        self._params["page"] = page
        self._params["limit"] = limit
        return self.list_movies()

    def reset_params(self):
        """Reset all parameters to default values"""
        self.__init__()

    def advanced_search(
        self,
        query_term: Optional[str] = None,
        quality: Optional[str] = None,
        genre: Optional[str] = None,
        rating: Optional[float] = None,
        sort_by: str = "date_added",
        order_by: str = "desc",
        limit: int = 20,
        page: int = 1,
        with_rt_ratings: bool = False
    ) -> List[Movie]:
        """
        Advanced search for movies with multiple parameters
        
        Args:
            query_term: Search term for movie title
            quality: Filter by quality (720p, 1080p, 2160p)
            genre: Filter by genre
            rating: Minimum rating
            sort_by: Sort results by (title, year, rating, peers, seeds, download_count, like_count, date_added)
            order_by: Sort order (desc, asc)
            limit: Number of results per page (1-50)
            page: Page number
            with_rt_ratings: Include Rotten Tomatoes ratings
        
        Returns:
            List[Movie]: List of movies matching the search criteria
        """
        search_params = {
            "query_term": query_term,
            "quality": quality,
            "genre": genre,
            "minimum_rating": rating,
            "sort_by": sort_by,
            "order_by": order_by,
            "limit": min(max(1, limit), 50),  # Ensure limit is between 1 and 50
            "page": max(1, page),  # Ensure page is at least 1
            "with_rt_ratings": with_rt_ratings
        }
        
        # Remove None values
        search_params = {k: v for k, v in search_params.items() if v is not None}
        
        # Update current params
        self._params.update(search_params)
        
        return self.list_movies()

    def get_movie_poster(self, movie_name: str) -> Optional[dict]:
        """
        Quickly fetch a movie's poster URLs by title
        
        Args:
            movie_name: Name of the movie to search for
        
        Returns:
            Optional[dict]: Dictionary containing poster URLs or None if not found
            {
                'small': small_cover_image,
                'medium': medium_cover_image,
                'large': large_cover_image
            }
        """
        search_params = {
            "query_term": movie_name,
            "limit": 1,  # Only get first result for speed
        }
        
        try:
            response = self._make_request("list_movies.json", search_params)
            if (response["status"] == "ok" and 
                "data" in response and 
                "movies" in response["data"] and 
                response["data"]["movies"]):
                
                movie = response["data"]["movies"][0]
                return {
                    "small": movie["small_cover_image"],
                    "medium": movie["medium_cover_image"],
                    "large": movie["large_cover_image"]
                }
        except Exception as e:
            print(f"Error fetching poster for {movie_name}: {str(e)}")
        
        return None

if __name__ == "__main__":
    yts = YTSService()
    print(yts.get_movie_poster("The Matrix").get("medium"))
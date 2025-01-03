from typing import Optional, Dict, Any, List
import requests
import time
from urllib.parse import urljoin
from functools import lru_cache

class TVDBService:
    BASE_URL = "https://api.thetvdb.com/api/"
    
    def __init__(self, api_key: str = "e861902c-17b9-464d-82b0-c6169747a224"):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.params = {'apikey': self.api_key}
        
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
    def search_series(self, name: str) -> List[Dict]:
        """Search for TV series by name"""
        return self._make_request("search/series", params={"name": name})

    @lru_cache(maxsize=128)
    def get_series(self, series_id: int) -> Dict:
        """Get series details by ID"""
        return self._make_request(f"series/{series_id}")

    @lru_cache(maxsize=128)
    def get_series_episodes(self, series_id: int) -> List[Dict]:
        """Get episodes for a series"""
        return self._make_request(f"series/{series_id}/episodes")

    @lru_cache(maxsize=128)
    def get_episode(self, episode_id: int) -> Dict:
        """Get episode details by ID"""
        return self._make_request(f"episodes/{episode_id}")

    @lru_cache(maxsize=128)
    def get_series_images(self, series_id: int) -> List[Dict]:
        """Get images for a series"""
        return self._make_request(f"series/{series_id}/images")

    @lru_cache(maxsize=128)
    def get_series_poster(self, series_id: int) -> str:
        """Get poster URL for a series"""
        images = self.get_series_images(series_id)
        if images and "data" in images:
            posters = [img for img in images["data"] if img.get("keyType") == "poster"]
            if posters:
                # Sort by rating and get highest rated poster
                posters.sort(key=lambda x: float(x.get("ratingsInfo", {}).get("average", 0)), reverse=True)
                return urljoin(self.BASE_URL, posters[0].get("fileName", ""))
        return ""

if __name__ == "__main__":
    # Initialize service
    tvdb = TVDBService()
    
    # Test search
    print("\n=== Search Results ===")
    search_query = "Breaking Bad"
    search_results = tvdb.search_series(search_query)
    if "data" in search_results:
        for result in search_results["data"]:
            print(f"Series: {result.get('seriesName')} ({result.get('firstAired', 'N/A')})")
            series_id = result.get('id')
            if series_id:
                # Test getting series details
                series = tvdb.get_series(series_id)
                if "data" in series:
                    print(f"Overview: {series['data'].get('overview', 'N/A')[:200]}...")
                
                # Test getting poster
                poster_url = tvdb.get_series_poster(series_id)
                if poster_url:
                    print(f"Poster URL: {poster_url}")
                
                # Test getting episodes
                episodes = tvdb.get_series_episodes(series_id)
                if "data" in episodes:
                    print(f"Total Episodes: {len(episodes['data'])}")
                print("\n")
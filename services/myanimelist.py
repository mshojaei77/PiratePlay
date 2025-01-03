from typing import Dict, List
import requests
from functools import lru_cache

class MyAnimeListService:
    BASE_URL = "https://api.myanimelist.net/v2"
    
    def __init__(self, client_id: str = "c35bc7853d0c090037068752df9fee9f"):
        self.client_id = client_id
        self.session = requests.Session()
        self.session.headers.update({
            'X-MAL-CLIENT-ID': self.client_id
        })

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with error handling"""
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {str(e)}")
            return {"results": []}

    @lru_cache(maxsize=128)
    def get_trending_anime(self) -> Dict[str, List]:
        """Get trending/seasonal anime"""
        params = {
            'ranking_type': 'all',
            'limit': 20,
            'fields': 'id,title,main_picture,mean'
        }
        response = self._make_request('anime/ranking', params)
        
        if not response:
            return {"results": []}
            
        # Transform response to match TMDB format
        results = []
        seen_titles = set()
        for item in response.get('data', []):
            node = item.get('node', {})
            title = node.get('title')
            
            # Skip if we've already seen this title
            if title in seen_titles:
                continue
                
            seen_titles.add(title)
            results.append({
                'id': node.get('id'),
                'name': title,
                'poster_path': node.get('main_picture', {}).get('large'),
                'vote_average': node.get('mean')
            })
            
        return {"results": results}

    @lru_cache(maxsize=128)
    def get_anime_poster_by_id(self, anime_id: int) -> str:
        """Get anime poster URL directly by ID"""
        params = {
            'fields': 'main_picture'
        }
        response = self._make_request(f'anime/{anime_id}', params)
        if response and 'main_picture' in response:
            return response['main_picture'].get('large', '')
        return ""

    def get_anime_details(self, anime_id: int) -> Dict:
        """Get detailed information about a specific anime"""
        params = {
            'fields': 'id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,media_type,status,genres,num_episodes,start_season,broadcast,source,rating,studios'
        }
        return self._make_request(f'anime/{anime_id}', params)

    def search_anime(self, query: str, limit: int = 100) -> Dict:
        """Search for anime by name"""
        params = {
            'q': query,
            'limit': min(limit, 100),
            'fields': 'id,title,main_picture,mean,media_type,num_episodes'
        }
        return self._make_request('anime', params)

    def get_seasonal_anime(self, year: int, season: str, limit: int = 100, sort: str = 'anime_score') -> Dict:
        """Get seasonal anime
        season: 'winter', 'spring', 'summer', 'fall'
        sort: 'anime_score' or 'anime_num_list_users'
        """
        if season not in ['winter', 'spring', 'summer', 'fall']:
            raise ValueError("Season must be one of: winter, spring, summer, fall")
            
        params = {
            'sort': sort,
            'limit': min(limit, 500),
            'fields': 'id,title,main_picture,mean,media_type,num_episodes'
        }
        return self._make_request(f'anime/season/{year}/{season}', params)
    def get_anime_ranking(self, ranking_type: str = 'all', limit: int = 100) -> Dict:
        """Get anime ranking by different types
        ranking_type: 'all', 'airing', 'upcoming', 'tv', 'ova', 'movie', 'special', 'bypopularity', 'favorite'
        """
        valid_types = ['all', 'airing', 'upcoming', 'tv', 'ova', 'movie', 'special', 'bypopularity', 'favorite']
        if ranking_type not in valid_types:
            raise ValueError(f"Ranking type must be one of: {', '.join(valid_types)}")

        params = {
            'ranking_type': ranking_type,
            'limit': min(limit, 500),
            'fields': 'id,title,main_picture,mean,rank,popularity'
        }
        response = self._make_request('anime/ranking', params)
        
        results = []
        if response and 'data' in response:
            for item in response['data']:
                node = item['node']
                results.append({
                    'id': node.get('id'),
                    'name': node.get('title'),
                    'poster_path': node.get('main_picture', {}).get('large'),
                    'vote_average': node.get('mean'),
                    'rank': item['ranking'].get('rank'),
                    'popularity': node.get('popularity')
                })
                
        return {"results": results}

# Usage example        
if __name__ == "__main__":
    # Initialize service
    mal = MyAnimeListService()

    trending = mal.get_trending_anime()
    for anime in trending['results']:
        print(mal.get_anime_poster_by_id(anime['id']))

import logging
import requests
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
import time

from .config import config

logger = logging.getLogger(__name__)

class WebSearch:
    def __init__(self):
        self.config = config.get_web_search_config()
        self.enabled = self.config.get('enabled', True)
        self.providers = self.config.get('providers', ['duckduckgo'])
        self.max_results = self.config.get('max_results', 5)
        self.search_timeout = self.config.get('search_timeout', 10)
        self.serpapi_key = self.config.get('serpapi_key', '')
        
        logger.info(f"WebSearch initialized with providers: {self.providers}")
    
    def search(self, query: str, provider: Optional[str] = None, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """Search the web for the given query."""
        if not self.enabled:
            logger.info("Web search is disabled")
            return []
        
        if not query.strip():
            logger.warning("Empty query provided")
            return []
        
        # Use specified max_results or default
        max_results = max_results or self.max_results
        
        # Use specified provider or first available provider
        if provider and provider in self.providers:
            search_provider = provider
        else:
            search_provider = self.providers[0] if self.providers else 'duckduckgo'
        
        try:
            if search_provider == 'duckduckgo':
                return self._search_duckduckgo(query, max_results)
            elif search_provider == 'serpapi':
                return self._search_serpapi(query, max_results)
            else:
                logger.warning(f"Unknown search provider: {search_provider}")
                return []
                
        except Exception as e:
            logger.error(f"Error during web search: {e}")
            return []
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo."""
        try:
            results = []
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=max_results)
                
                for result in search_results:
                    if result:
                        search_result = {
                            'title': result.get('title', ''),
                            'snippet': result.get('body', ''),
                            'url': result.get('link', ''),
                            'provider': 'duckduckgo'
                        }
                        results.append(search_result)
            
            logger.info(f"DuckDuckGo search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error in DuckDuckGo search: {e}")
            return []
    
    def _search_serpapi(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using SerpAPI."""
        if not self.serpapi_key:
            logger.warning("SerpAPI key not configured")
            return []
        
        try:
            url = "https://serpapi.com/search"
            params = {
                'q': query,
                'api_key': self.serpapi_key,
                'num': max_results
            }
            
            response = requests.get(url, params=params, timeout=self.search_timeout)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Extract organic results
            organic_results = data.get('organic_results', [])
            for result in organic_results[:max_results]:
                search_result = {
                    'title': result.get('title', ''),
                    'snippet': result.get('snippet', ''),
                    'url': result.get('link', ''),
                    'provider': 'serpapi'
                }
                results.append(search_result)
            
            logger.info(f"SerpAPI search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error in SerpAPI search: {e}")
            return []
    
    def format_search_results(self, results: List[Dict[str, Any]]) -> str:
        """Format search results into a readable string."""
        if not results:
            return ""
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_result = f"{i}. {result['title']}\n"
            formatted_result += f"   URL: {result['url']}\n"
            formatted_result += f"   {result['snippet']}\n"
            formatted_results.append(formatted_result)
        
        return "\n".join(formatted_results)
    
    def get_search_summary(self, results: List[Dict[str, Any]]) -> str:
        """Get a summary of search results."""
        if not results:
            return "No web search results found."
        
        summary = f"Found {len(results)} relevant web search results:\n\n"
        for i, result in enumerate(results, 1):
            summary += f"{i}. {result['title']} - {result['url']}\n"
        
        return summary

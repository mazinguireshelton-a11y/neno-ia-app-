"""
Plugin de busca na web para a NENO IA
"""
import os
import requests
from typing import List, Dict
import json
import logging

logger = logging.getLogger(__name__)

class WebSearchPlugin:
    def __init__(self):
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.serpapi_key = os.getenv("SERPAPI_KEY")
        self.google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.google_cx = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    def execute(self, query: str, num_results: int = 5) -> Dict:
        """Executa busca na web"""
        try:
            # Tenta Serper primeiro
            if self.serper_api_key:
                results = self._search_serper(query, num_results)
            # Fallback para SerpAPI
            elif self.serpapi_key:
                results = self._search_serpapi(query, num_results)
            # Fallback para Google Custom Search
            elif self.google_api_key and self.google_cx:
                results = self._search_google(query, num_results)
            else:
                return {"error": "Nenhum serviço de busca configurado"}
                
            return {"results": results, "count": len(results)}
            
        except Exception as e:
            logger.error(f"Erro na busca web: {e}")
            return {"error": str(e)}
    
    def _search_serper(self, query: str, num_results: int) -> List[Dict]:
        """Busca usando Serper API"""
        url = "https://google.serper.dev/search"
        
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        
        data = {"q": query, "num": num_results}
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        
        results = []
        data = response.json()
        
        # Extrai resultados orgânicos
        if "organic" in data:
            for item in data["organic"]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return results
    
    def _search_serpapi(self, query: str, num_results: int) -> List[Dict]:
        """Busca usando SerpAPI"""
        params = {
            "q": query,
            "api_key": self.serpapi_key,
            "engine": "google",
            "num": num_results
        }
        
        response = requests.get("https://serpapi.com/search", params=params, timeout=15)
        response.raise_for_status()
        
        results = []
        data = response.json()
        
        if "organic_results" in data:
            for item in data["organic_results"]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return results
    
    def _search_google(self, query: str, num_results: int) -> List[Dict]:
        """Busca usando Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        
        params = {
            "q": query,
            "key": self.google_api_key,
            "cx": self.google_cx,
            "num": min(num_results, 10)  # Google limita a 10 resultados
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        results = []
        data = response.json()
        
        if "items" in data:
            for item in data["items"]:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
        
        return results

def register():
    return WebSearchPlugin()

import logging
import asyncio
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

def search_sync(query: str):
    """Run synchronous duckduckgo search"""
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=7))

async def collect_market_data(sector: str) -> str:
    """Web search DuckDuckGo API for recent stock market news"""
    query = f"{sector} India stock market news today"
    logger.info(f"Searching DuckDuckGo for: {query}")
    
    try:
        # We run the synchronous API in a thread pool to avoid blocking the FastAPI event loop
        results = await asyncio.to_thread(search_sync, query)
        
        if not results:
            return "No recent news found for this sector."
        
        # Format results into a context string
        context_lines = []
        for idx, res in enumerate(results):
            context_lines.append(f"Source {idx+1}:\nTitle: {res.get('title')}\nSnippet: {res.get('body')}\n")
        
        return "\n".join(context_lines)
    except Exception as e:
        logger.error(f"Error collecting data: {e}")
        raise Exception(f"DuckDuckGo search error: {e}")

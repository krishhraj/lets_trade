import time
import logging
from fastapi import APIRouter, Depends, Request, HTTPException, Path
from ..core.security import get_api_key
from ..core.rate_limiter import limiter
from ..models.pydantic_models import AnalysisResponse
from ..services.data_collector import collect_market_data
from ..services.ai_analyzer import analyze_sector

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory dictionary cache: sector_key -> (timestamp, report)
# Cache Time-To-Live = 10 minutes
CACHE_TTL = 600 
response_cache = {}

@router.get("/analyze/{sector}", response_model=AnalysisResponse)
@limiter.limit("10/minute")
async def analyze_endpoint(
    request: Request,
    sector: str = Path(..., min_length=2, max_length=50, pattern="^[a-zA-Z0-9_-]+$", description="Sector to analyze"),
    api_key: str = Depends(get_api_key)
):
    """
    GET `/analyze/{sector}`
    Analyzes Indian stock market trade opportunities for a given sector using DuckDuckGo and Google Gemini.
    """
    sector_key = sector.lower().strip()
    current_time = time.time()
    
    # 1. Check Cache
    if sector_key in response_cache:
        cached_time, cached_report = response_cache[sector_key]
        if current_time - cached_time < CACHE_TTL:
            logger.info(f"Serving cached response for sector: {sector_key}")
            return AnalysisResponse(sector=sector, markdown_report=cached_report)
    
    # 2. Gather context from web
    try:
        search_data = await collect_market_data(sector_key)
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        raise HTTPException(status_code=502, detail=str(e))
        
    # 3. Analyze with Gemini
    try:
        report = await analyze_sector(sector_key, search_data)
    except Exception as e:
        logger.error(f"AI Analysis failed: {e}")
        raise HTTPException(status_code=502, detail=str(e))
        
    # 4. Save to Cache
    response_cache[sector_key] = (current_time, report)
    
    # 5. Return JSON payload matching response format
    return AnalysisResponse(sector=sector, markdown_report=report)

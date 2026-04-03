import os
import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

def configure_gemini():
    """Configure Gemini with environment API Key"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
         logger.warning("GEMINI_API_KEY environment variable is not set. Service might fail if it's missing.")
    genai.configure(api_key=api_key)

async def analyze_sector(sector: str, search_results: str) -> str:
    """Analyze the sector news using Google Gemini"""
    configure_gemini()
    
    prompt = (
        f"Analyze trade opportunities in the '{sector}' sector in the Indian stock market "
        f"based on this market data:\n\n{search_results}\n\n"
        f"Provide the response as a well-structured MARKDOWN report."
    )
    
    try:
        # Using gemini-2.5-flash based on API key access rules
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Async generation
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error analyzing with Gemini: {e}")
        raise Exception(f"Failed to generate AI analysis: {e}")

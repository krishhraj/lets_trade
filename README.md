# Letstrade Sector Analysis API

A production-ready FastAPI service for Indian sector trade analysis.
This service automates the workflow of searching for fresh stock market news using DuckDuckGo, analyzing the findings via Google Gemini AI, and returning structured MARKDOWN reports.

## Features
- **FastAPI Backend**: Async standard routing
- **Pydantic Validation**: Strong request/response type checking
- **SlowAPI Rate Limiting**: 10 requests per minute by default
- **Simple API Key Security**: Securing endpoints
- **In-memory Caching**: Improves performance and limits API stress
- **DuckDuckGo Web Search**: Up-to-date query gathering
- **Google Gemini Analysis**: Actionable AI reports formatted in markdown

## Setup & Running Locally

1. **Install Dependencies**
   Ensure you have Python installed, then run:

   ```bash
   pip install fastapi uvicorn slowapi duckduckgo-search google-generativeai pydantic
   ```

2. **Environment Variables**
   Set the API Key for your server and your Google Gemini key.

   *Windows (PowerShell):*
   ```powershell
   $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
   $env:API_KEY="your-secret-api-key"
   ```

   *(Optional: If `API_KEY` is not provided, it defaults to `default-dev-key` for dev purposes)*

3. **Start the Application**
   For running locally or in production:

   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the Application**
   - The interactive API documentation (Swagger) is auto-generated at: `http://127.0.0.1:8000/docs`
   - Make a sample curl request:
   ```bash
   curl -H "X-API-Key: default-dev-key" http://127.0.0.1:8000/analyze/pharmaceuticals
   ```

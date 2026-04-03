import os
import logging
from fastapi import FastAPI, Request

# Basic custom .env loader to prevent terminal export issues
try:
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ[k] = v.strip('"\'')
except FileNotFoundError:
    pass

from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .core.rate_limiter import limiter
from .routers import analysis

# Setup basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Letstrade Sector Analysis API",
    description="Production-ready FastAPI service for Indian sector trade analysis leveraging Gemini and DuckDuckGo.",
    version="1.0.0"
)

# 1. Set up slowapi
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "path": request.url.path
        },
    )

# 3. Include Routers
app.include_router(analysis.router)

if __name__ == "__main__":
    import uvicorn
    # This allows it to easily be runnable locally
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

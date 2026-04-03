import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

# API Key Validation (Simple security standard)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """Validate API Key provided in header"""
    expected_api_key = os.environ.get("API_KEY", "default-dev-key")
    if api_key == expected_api_key:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate API KEY",
    )

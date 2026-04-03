from slowapi import Limiter
from slowapi.util import get_remote_address

# Limit to 10 requests per minute by default
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

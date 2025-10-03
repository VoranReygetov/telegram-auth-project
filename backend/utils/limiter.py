from slowapi import Limiter
from slowapi.util import get_remote_address

# Create rate limiter using client IP as key
limiter = Limiter(key_func=get_remote_address)

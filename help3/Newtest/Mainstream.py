from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request
from starlette.responses import JSONResponse

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# Global exception handler for rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(content={"detail": "Rate limit exceeded"}, status_code=429)

@app.get("/limited")
@limiter.limit("2/minute")  # Allow only 2 requests per minute
async def limited_endpoint():
    return {"message": "Success"}

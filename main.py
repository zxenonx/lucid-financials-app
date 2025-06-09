from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager
import anyio

from app.config.settings import settings
from app.config.database import init_database

try:
    from app.models.user import User
    logging.info("All models imported successfully")
except ImportError as e:
    logging.warning(f"Some models not found: {e}")

from app.controllers.auth_controller import auth_router
from app.controllers.post_controller import post_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await anyio.to_thread.run_sync(init_database)
    yield

app = FastAPI(
    title="Lucid Blog API",
    description="A FastAPI web app following MVC pattern with MySQL database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if hasattr(settings, 'ALLOWED_ORIGINS') else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_size_middleware(request: Request, call_next):
    """
    Middleware to validate request payload size.

    Ensures that incoming requests do not exceed the maximum allowed size
    of 1MB as specified in the requirements.

    Args:
        request (Request): The incoming HTTP request
        call_next: The next middleware or route handler

    Returns:
        Response: The HTTP response or error if payload too large

    Raises:
        HTTPException: 413 error if payload exceeds 1MB limit
    """
    max_size = settings.MAX_PAYLOAD_SIZE_MB * 1024 * 1024

    if request.headers.get("content-length"):
        content_length = int(request.headers["content-length"])
        if content_length > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"Payload too large. Maximum size is {settings.MAX_PAYLOAD_SIZE_MB}MB"
            )

    return await call_next(request)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions.

    Args:
        request (Request): The HTTP request that caused the exception
        exc (Exception): The exception that was raised

    Returns:
        JSONResponse: Standardized error response
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": "An unexpected error occurred"
        }
    )

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    post_router,
    prefix="/api/v1/posts",
    tags=["Posts"]
)


@app.get("/")
async def root():
    """
    Root endpoint for API health check.
    """
    return {
        "message": "Welcome to Lucid Blog API",
        "status": "running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

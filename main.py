import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers.auth import router as auth_router
from routers.recommendations import router as recommendations_router
from src.database import create_db_and_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create database and tables on startup
app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status code: {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(recommendations_router, prefix="/recommendations", tags=["recommendations"])

@app.get("/")
def home():
    logger.info("Root endpoint accessed")
    return {"mensaje": "API de recomendación de películas"}

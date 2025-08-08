from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.recommendations import router as recommendations_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(recommendations_router, prefix="/recommendations", tags=["recommendations"])

@app.get("/")
def home():
    return {"mensaje": "API de recomendación de películas"}
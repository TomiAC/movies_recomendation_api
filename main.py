from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "API de recomendación de películas"}

@app.get("/recomendacion/{user_id}")
def recomendacion(user_id: int):
    return {"mensaje": f"Recomendaciones para el usuario {user_id}"}

@app.get("recomendacion/nuevo_usuario/{user_id}")
def recomendacion_nuevo_usuario(user_id: int):
    return {"mensaje": f"Recomendaciones para el usuario {user_id}"}

@app.get("/populares")
def populares():
    return {"mensaje": "Películas populares"}
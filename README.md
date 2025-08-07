# 🎬 Movie Recommender API

Una API para recomendar películas basada en aprendizaje automático (colaborativo y por contenido), usando Python y FastAPI.

## Endpoints

- `GET /recomendar/{user_id}` → Recomendaciones colaborativas
- `POST /recomendar/nuevo_usuario` → Recomendaciones para nuevos usuarios
- `GET /populares` → Películas más populares

## Cómo correr el proyecto

```bash
fastapi dev main.py
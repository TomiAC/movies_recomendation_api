# Films Recommendation API

<details>
<summary>English</summary>

This project implements a film recommendation API using various recommendation algorithms, including collaborative filtering, content-based filtering, and a hybrid approach. The API is built with FastAPI and provides endpoints for user authentication and film recommendations.

## Features

*   **User Authentication:** Secure user registration and login.
*   **Collaborative Filtering:** Recommendations based on user-item interactions (e.g., ratings).
*   **Content-Based Filtering:** Recommendations based on film attributes (e.g., genres, keywords).
*   **Hybrid Recommendations:** Combines collaborative and content-based approaches for improved accuracy.
*   **Popularity-Based Recommendations:** Fallback recommendations based on overall film popularity.
*   **RESTful API:** Built with FastAPI for efficient and scalable access.

## Technologies Used

*   Python 3.9+
*   FastAPI
*   SQLAlchemy (for database interactions)
*   Pandas (for data manipulation)
*   Scikit-learn (for machine learning models, e.g., TF-IDF)
*   Joblib (for saving/loading precomputed data)
*   SQLite (default database)

## Project Structure

*   `main.py`: Main application entry point.
*   `routers/`: Contains API route definitions (e.g., `auth.py`, `recommendations.py`).
*   `src/`: Core logic for recommendation algorithms, database models, and utilities.
    *   `colaborative.py`: Collaborative filtering implementation.
    *   `content.py`: Content-based filtering implementation.
    *   `hybrid.py`: Hybrid recommendation system.
    *   `popularity.py`: Popularity-based recommendations.
    *   `database.py`: Database connection and session management.
    *   `models.py`: SQLAlchemy ORM models.
    *   `matrix_builder.py`: Logic for building user-item and TF-IDF matrices.
    *   `utils.py`: Helper functions.
*   `datasets/`: Stores raw dataset files (e.g., `movies.csv`, `ratings.csv`).
*   `precomputed_data/`: Stores precomputed data (e.g., TF-IDF matrix, user-item matrix) for faster recommendations.
*   `scripts/`: Utility scripts for data loading and precomputation.
    *   `load_initial_data.py`: Script to load initial data from CSVs into the database.
    *   `precompute_data.py`: Script to precompute necessary data for recommendation algorithms.
*   `tests/`: Unit and integration tests.
*   `recommendations.db`: SQLite database file (generated after running data loading script).
*   `requirements.txt`: Project dependencies.

## Setup and Installation

Follow these steps to set up and run the project locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/films_recommendation_api.git
    cd films_recommendation_api
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare the database and load initial data:**
    This step will create the `recommendations.db` SQLite file and populate it with data from the `datasets` folder.
    ```bash
    python scripts/load_initial_data.py
    ```

5.  **Precompute recommendation data:**
    This script will generate and save the necessary matrices and data structures in the `precomputed_data` directory, which are crucial for the recommendation algorithms.
    ```bash
    python scripts/precompute_data.py
    ```

## Running the API

To start the FastAPI application, use Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be accessible at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Running Tests

To run the project's tests, ensure your virtual environment is active and run pytest:

```bash
pytest
```

</details>

<details>
<summary>Español</summary>

Este proyecto implementa una API de recomendación de películas utilizando varios algoritmos de recomendación, incluyendo filtrado colaborativo, filtrado basado en contenido y un enfoque híbrido. La API está construida con FastAPI y proporciona endpoints para la autenticación de usuarios y recomendaciones de películas.

## Características

*   **Autenticación de Usuarios:** Registro e inicio de sesión de usuarios seguros.
*   **Filtrado Colaborativo:** Recomendaciones basadas en interacciones usuario-item (por ejemplo, calificaciones).
*   **Filtrado Basado en Contenido:** Recomendaciones basadas en atributos de las películas (por ejemplo, géneros, palabras clave).
*   **Recomendaciones Híbridas:** Combina enfoques colaborativos y basados en contenido para una mayor precisión.
*   **Recomendaciones Basadas en Popularidad:** Recomendaciones de respaldo basadas en la popularidad general de las películas.
*   **API RESTful:** Construida con FastAPI para un acceso eficiente y escalable.

## Tecnologías Utilizadas

*   Python 3.9+
*   FastAPI
*   SQLAlchemy (para interacciones con la base de datos)
*   Pandas (para manipulación de datos)
*   Scikit-learn (para modelos de machine learning, ej., TF-IDF)
*   Joblib (para guardar/cargar datos precalculados)
*   SQLite (base de datos por defecto)

## Estructura del Proyecto

*   `main.py`: Punto de entrada principal de la aplicación.
*   `routers/`: Contiene las definiciones de las rutas de la API (ej., `auth.py`, `recommendations.py`).
*   `src/`: Lógica principal para los algoritmos de recomendación, modelos de base de datos y utilidades.
    *   `colaborative.py`: Implementación del filtrado colaborativo.
    *   `content.py`: Implementación del filtrado basado en contenido.
    *   `hybrid.py`: Sistema de recomendación híbrido.
    *   `popularity.py`: Recomendaciones basadas en popularidad.
    *   `database.py`: Conexión y gestión de sesiones de la base de datos.
    *   `models.py`: Modelos ORM de SQLAlchemy.
    *   `matrix_builder.py`: Lógica para construir las matrices usuario-item y TF-IDF.
    *   `utils.py`: Funciones de ayuda.
*   `datasets/`: Almacena los archivos de datos brutos (ej., `movies.csv`, `ratings.csv`).
*   `precomputed_data/`: Almacena datos precalculados (ej., matriz TF-IDF, matriz usuario-item) para recomendaciones más rápidas.
*   `scripts/`: Scripts de utilidad para la carga y precomputo de datos.
    *   `load_initial_data.py`: Script para cargar los datos iniciales desde los CSVs a la base de datos.
    *   `precompute_data.py`: Script para precalcular los datos necesarios para los algoritmos de recomendación.
*   `tests/`: Pruebas unitarias y de integración.
*   `recommendations.db`: Archivo de la base de datos SQLite (generado después de ejecutar el script de carga de datos).
*   `requirements.txt`: Dependencias del proyecto.

## Configuración e Instalación

Sigue estos pasos para configurar y ejecutar el proyecto localmente:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/your-username/films_recommendation_api.git
    cd films_recommendation_api
    ```

2.  **Crea un entorno virtual y actívalo:**
    ```bash
    python -m venv .venv
    # En Windows
    .venv\Scripts\activate
    # En macOS/Linux
    source .venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepara la base de datos y carga los datos iniciales:**
    Este paso creará el archivo SQLite `recommendations.db` y lo poblará con datos de la carpeta `datasets`.
    ```bash
    python scripts/load_initial_data.py
    ```

5.  **Precalcula los datos de recomendación:**
    Este script generará y guardará las matrices y estructuras de datos necesarias en el directorio `precomputed_data`, que son cruciales para los algoritmos de recomendación.
    ```bash
    python scripts/precompute_data.py
    ```

## Ejecutando la API

Para iniciar la aplicación FastAPI, usa Uvicorn:

```bash
uvicorn main:app --reload
```

La API será accesible en `http://127.0.0.1:8000`. Puedes acceder a la documentación interactiva de la API (Swagger UI) en `http://127.0.0.1:8000/docs`.

## Ejecutando las Pruebas

Para ejecutar las pruebas del proyecto, asegúrate de que tu entorno virtual esté activo y ejecuta pytest:

```bash
pytest
```

</details>

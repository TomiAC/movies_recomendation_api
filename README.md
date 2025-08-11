# Films Recommendation API

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
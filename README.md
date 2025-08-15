# Book Recommendation API

This project is a Python-based book recommendation system built with FastAPI. It provides two types of recommendations:

- **Collaborative Filtering:** Recommends books to a user based on the ratings of similar users.
- **Content-Based Filtering:** Recommends books similar to a given book based on its title, author, and genre.

## Project Structure

- `api/`: Contains the FastAPI application.
  - `main.py`: The main application file with the API endpoints.
  - `recommendations.py`: The core recommendation logic.
  - `models.py`: The Pydantic data models.
- `data/`: Contains the sample datasets.
  - `books.csv`: A list of books with their metadata.
  - `ratings.csv`: A list of user ratings for books.
- `notebooks/`: Contains a Jupyter notebook for exploratory data analysis.
  - `eda.ipynb`: A notebook for exploring and visualizing the data.
- `requirements.txt`: The project dependencies.

## Getting Started

1. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**

   ```bash
   uvicorn api.main:app --reload
   ```

3. **Access the API documentation:**

   Open your browser and go to `http://127.0.0.1:8000/docs`.

## API Endpoints

- `GET /recommendations/user/{user_id}`: Get book recommendations for a user.
- `GET /recommendations/book/{book_id}`: Get book recommendations based on a book. You can specify the data type to use for the recommendation with the `data_type` query parameter. The options are `structured` (default) and `unstructured`.
  - Example: `http://127.0.0.1:8000/recommendations/book/1?data_type=unstructured`
- `GET /recommendations/model/{user_id}`: Get model-based book recommendations for a user.
- `GET /recommendations/cluster/{book_id}`: Get cluster-based book recommendations for a user.

## Docker

This project includes a `Dockerfile` to containerize the application.

### Build the Docker Image

```bash
docker build -t book-recommendation-api .
```

### Run the Docker Container

```bash
docker run -d -p 8000:8000 book-recommendation-api
```

## Unit Tests

This project uses `pytest` for unit testing.

### Run the Tests

To run the tests, first install the testing dependencies:

```bash
pip install pytest httpx
```

Then, run the tests from the root of the project:

```bash
pytest
```

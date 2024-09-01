# Movie Recommendation System

## Overview

This project implements a scalable Movie Recommendation System that leverages a multi-stage pipeline with ETL, model training, and an API for serving recommendations. The entire system is containerized using Docker and includes load testing using Locust.

## Features

- **ETL Pipeline**: Extracts and transforms movie data, then saves it to an S3-compatible storage (MinIO).
- **Model Training**: Loads data from S3, trains the recommendation model, and saves the trained model back to S3.
- **API Service**: A FastAPI-based service that loads the model from S3 and serves movie recommendations.
- **Load Testing**: Uses Locust to test the API's performance under load.

## Project Structure

- `Dockerfile`: Configuration for building the application container.
- `docker-compose.yml`: Defines services for ETL, model training, API, and MinIO.
- `locustfile.py`: Script for load testing the API.
- `src/`: Source code for ETL, training, and API.
- `data/`: Initial data files used by the ETL process.

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/olawale0254/Movie_recommendation.git
   cd Movie_recommendation
   ```

2. ** Environment Variables: Create a `.env` file in the root directory with your MinIO credentials:
   ```bash
   S3_ACCESS_KEY=<your-access-key>
   S3_SECRET_KEY=<your-secret-key>
   ```
3. ** Build and Run the Application:
   ```bash
   docker-compose up --build
   ```
4. Access the Services:
   - API: `http://localhost:8000`
   - MinIO Console: `http://localhost:9001`
## Pipeline Overview
- ETL Service: Loads and processes movie data, then stores it in MinIO (S3-compatible storage).
- Trainer Service: Retrieves the processed data from MinIO, trains the model, and saves the model back to MinIO.
- API Service: Loads the trained model from MinIO and provides movie recommendations via RESTful endpoints.

## Load Testing
Use Locust to test the API's performance:
```bash
locust -f locustfile.py --host=http://localhost:8000
```

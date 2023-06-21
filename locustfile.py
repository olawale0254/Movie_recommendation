from locust import HttpUser, task, between
import random

class MovieRecommender(HttpUser):
    wait_time = between(1, 3)  # Add some wait time between requests

    @task
    def get_recommendation(self):
        movie_name = random.choice(['Titan A.E.', "Ender's Game", "Independence Day", 'Avatar', 'The Fifth Element', 'Star Trek Into Darkness', 'Jupiter Ascending', 'Battle: Los Angeles'])
        self.client.get(f"/predict?movie={movie_name}")

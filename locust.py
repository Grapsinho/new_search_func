from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Time between requests

    @task
    def all_product(self):
        # Define the API endpoint and request
        search_term = "green sneakers"
        self.client.get(f"/api/products/{search_term}")
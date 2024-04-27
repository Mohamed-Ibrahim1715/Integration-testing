from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 10) # Wait between 1 and 10 seconds between each task

    @task
    def register(self):
        # Define the data for the POST request
        data = {
            "username": "testuser",
            "password": "password"
        }
        # Send a POST request to the /register endpoint
        self.client.post("/register", data=data)
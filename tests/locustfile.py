from locust import HttpUser, task, between


class TaskUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_task(self):
        self.client.post("/tasks", json={
            "title": "Load Test",
            "priority": 1
        })
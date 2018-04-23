from locust import HttpLocust, TaskSet, task

headers = {'content-type': 'application/json'}
payload = {"content":"Testing", "description":"Just Testing!"}

class UserBehavior(TaskSet):

    @task(3)
    def login(self):
        self.client.post("/api/v1/entries", json=payload, headers=headers, catch_response=True)

    @task(2)
    def index(self):
        self.client.get("/api/v1/entries")

    @task(1)
    def profile(self):
        self.client.get("/api/v1/status")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000

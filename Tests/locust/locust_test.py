import json
import string
from locust import task, constant_pacing, HttpUser, LoadTestShape
import random
from config import cfg, logger


class DocUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    def on_start(self):
        self.login()

    @task
    def add_doc(self) -> None:
        transaction = self.add_doc.__name__
        headers = {
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": f"Bearer {self.token_id}",
        }
        letters = string.ascii_lowercase
        ran = random.choice([random.randint(1, 11), 3])
        body = {
            "name": ''.join(random.choice(letters) for _ in range(10)),
            "content": ''.join(random.choice(letters) for _ in range(20)),
            "referrals": ','.join(str(random.randint(1, 480)) for _ in range(ran))
        }
        with self.client.post("/add_docs", headers=headers, json=body, catch_response=True,
                              name=transaction) as request:
            pass


    def login(self) -> None:
        credentials = {"username": "12", "password": "12"}
        with self.client.post("/login", data=credentials, catch_response=True) as request:
            pass
        response_body = json.loads(request.text)
        self.token_id = response_body["access_token"]
        print(self.token_id)

    def on_stop(self):
        logger.debug(f"user stopped")


class StagesShape(LoadTestShape):
    stages = [
        {"duration": 20, "users": 1, "spawn_rate": 1},
        {"duration": 40, "users": 2, "spawn_rate": 1},
        {"duration": 60, "users": 4, "spawn_rate": 1},
        {"duration": 80, "users": 6, "spawn_rate": 1},
        {"duration": 100, "users": 8, "spawn_rate": 1},
    ]

    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data
        return None

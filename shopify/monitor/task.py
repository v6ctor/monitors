import random
import requests

class Task:

    def __init__(self, proxies, site, webhook, delay, task_id):
        self.proxies = proxies
        self.proxy = random.choice(self.proxies)
        self.site = site
        self.products = []
        self.webhook = webhook
        self.delay = delay

        self.task_id = task_id

    def rotate_proxies(self):
        self.proxy = random.choice(self.proxies)

    def test(self):
        print("Worker %s started!" % self.task_id)

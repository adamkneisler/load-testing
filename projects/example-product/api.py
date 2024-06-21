from locust import HttpLocust, TaskSet, task

import json

import utils
import globals as globals

class API(TaskSet):
    """
    Class to handle simulating requests to MSL API
    """
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        MASHERY_KEY = globals.MASHERY_KEY
        API_KEY = globals.API_KEY

        self.HEADERS = {"Api-Key": MASHERY_KEY,
                        "content-type": "application/json"} # mashery
        self.create_accounts()

    def create_accounts(self):
        """
        Create accounts in the MSL
        """
        payload = utils.account_create_payload()
        self.client.post("/accounts/",
                json.dumps(payload),
                headers=self.HEADERS)

    @task(5)
    def create_transaction(self):
        payload = utils.transaction_payload()
        self.client.post("/transaction/",
                json.dumps(payload),
                headers=self.HEADERS)

    @task(2)
    def create_redemption(self):
        coupon_code = utils.get_coupon_code()
        account = utils.get_account()
        payload = {
            "code": coupon_code,
            "qo_id": account['qo_id']
            }
        self.client.post("/coupon/",
                json.dumps(payload),
                headers=self.HEADERS)
    
    @task(20)
    def get_account(self):
        account = utils.get_account()
        qo_id = account['qo_id']
        self.client.get("/accounts/", 
                headers=self.HEADERS,
                params={"qo_id": qo_id})

    @task(8)
    def get_locations(self):
        self.client.get("/locations/", 
                headers=self.HEADERS)
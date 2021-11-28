import json
import requests
import time

class Data:
    def __init__(self):
        self.MAX_PAGE = 25
        self.params = {"per_page": self.MAX_PAGE, "page": 1}

    def total_page(self):
        return self.TOTAL_PER_PAGE

    def check_response(self, response):
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            print("\nOh noes, something went wrong!\n")
            time.sleep(2)


    def get_data(self):
        with open("credentials.json", 'r') as f:
            param = json.load(f)


            BASE_URL = "https://" + param["subdomain"] + ".zendesk.com/api/v2/tickets.json"
            response = requests.get(BASE_URL, params=self.params, auth=(param["email"], param["password"]))
            data = self.check_response(response)
        return data

    def get_one(self, id):
 
        with open("credentials.json", 'r') as f:

            param = json.load(f)
            BASE_URL = "https://"+param["subdomain"]+".zendesk.com/api/v2/tickets/"+id+".json"
            response = requests.get(BASE_URL, auth=(param["email"], param["password"]))
            data = self.check_response(response)
        return data



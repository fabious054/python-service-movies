import requests


class DatabaseConnector:
    def __init__(self, url, bearer):
        self.url = url
        self.bearer = bearer
    
    def connect(self):
        payload = {}
        headers = {
            'Authorization': self.bearer
        }
        response = requests.get(self.url, headers=headers, data=payload)
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    
    
import requests
import json

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self) -> None:
        self.SHEETY_ENDPOINT = "https://api.sheety.co/178b21c86acd124f8b551671aa235d53/flightDeals/prices"
        self.sheety_headers = {
            "Authorization": "Bearer jdvd7eismz6dm39fld8s63h4f5"
        }

    def get_sheet_data(self):
        sheety_response = requests.get(url=self.SHEETY_ENDPOINT, headers=self.sheety_headers)
        print(sheety_response.text)
        data = sheety_response.json()["prices"]
        with open("doc_save.json", "w") as file:
            json.dump(data, file, indent=4)

    def upload(self, data):
        sheety_params = {
            "price": {
                "iataCode": data["iataCode"],
            }
        }
        sheety_response = requests.put(url=f"{self.SHEETY_ENDPOINT}/{data['id']}", json=sheety_params, headers=self.sheety_headers)
        print(sheety_response.text)

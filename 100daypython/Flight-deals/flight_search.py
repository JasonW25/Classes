import requests
import datetime as dt
import json
import flight_data as fd
import notification_manager as nm

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self) -> None:
        self.headers = {
            "apikey":"   "
            }
        self.start_end = "https://tequila-api.kiwi.com"
        self.flight_list = []
        
    def city_iata(self, city):
        query = {
            "term": city,
            "location_types": "city"
        }
        response = requests.get(url=f"{self.start_end}/locations/query", params=query, headers=self.headers)
        code = response.json()["locations"][0]["code"]
        return code

    def get_flights(self, code, price):
        now = dt.datetime.now()
        then = now + dt.timedelta(weeks=26)
        query = {
            "fly_from":"city:LON",
            "fly_to": code,
            "date_from": now.strftime("%d/%m/%Y"),
            "date_to": then.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "curr": "GBP",
            "price_to": price
        }
        response = requests.get(url=f"{self.start_end}/v2/search", params=query, headers=self.headers)
        print(response.text)
        data = response.json()["data"]
        with open("flight_save.json", "w") as file:
            json.dump(data, file, indent=4)
        # with open("flight_save.json", "r") as file:
        #     data = json.load(file)

        for items in data:
            flight = fd.FlightData()
            flight.set_price(items["price"])
            flight.set_dep_city(items["cityFrom"])
            flight.set_dep_ap_iata(items["flyFrom"])
            flight.set_ar_city(items["cityTo"])
            flight.set_ar_ap_iata(items["flyTo"])
            flight.set_out_date(items["route"][0]["local_arrival"].split("T")[0])
            flight.set_in_date(items["route"][1]["local_arrival"].split("T")[0])
            self.flight_list.append(flight)
        
    def send_alert(self):
        message = ""
        email = nm.NotificationManager()
        for flights in self.flight_list:
            message += (f"New flight found: Only GBP:{flights.price} to fly from {flights.dep_city}-{flights.dep_ap_iata} to {flights.ar_city}-{flights.ar_ap_iata}, from {flights.out_date} to {flights.in_date}.\n\n")
        if message != "":
            email.email(message)
        else:
            print("no flights")

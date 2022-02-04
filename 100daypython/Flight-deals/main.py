#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import data_manager as dm
import json
import flight_search

data_man = dm.DataManager()
f_search = flight_search.FlightSearch()

with open("doc_save.json", "r") as file:
    sheet_data = json.load(file)

update = input("Do you want to update the data from the spreadsheet (Yes or No):").lower()

if update == "yes":
    data_man.get_sheet_data()
    with open("doc_save.json", "r") as file:
        sheet_data = json.load(file)

change = False
for city in sheet_data:
    if city["iataCode"] == "":
        code = f_search.city_iata(city["city"])
        city["iataCode"] = code
        change = True
        data_man.upload(city)

if change == True:
    with open("doc_save.json", "w") as file:
            json.dump(sheet_data, file, indent=4)

for city in sheet_data:
    f_search.get_flights(city["iataCode"], city["lowestPrice"])
f_search.send_alert()

import requests
import datetime as dt

NUTRIX_API = ""
NUTRIX_ID = ""
NUTRIX_API_ENDPOINT = "h"

SHEETY_ENDPOINT = ""

today = dt.datetime.now()

nutrix_headers = {
    "x-app-id": NUTRIX_ID,
    "x-app-key": NUTRIX_API,
    "x-remote-user-id":"0"
}

nutrix_params = {
    "query": "biked for 5 miles",
    "gender": "male",
    "weight_kg": "95",
    "height_cm": "190",
    "age": "31",
}

n_response = requests.post(url=NUTRIX_API_ENDPOINT, json=nutrix_params, headers=nutrix_headers)
nutrix_response = n_response.json()

exercise = nutrix_response["exercises"][0]["name"].title()
duration = nutrix_response["exercises"][0]["duration_min"]
calories = nutrix_response["exercises"][0]["nf_calories"]

sheety_headers = {
    "Authorization": "Bearer ejjd8cvghe30msu"
}

sheety_params = {
    "workout": {
        "date": today.strftime("%d/%m/%Y"),
        "time": today.strftime("%H:%M:%S"),
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_params, headers=sheety_headers)

print(sheety_response.text)

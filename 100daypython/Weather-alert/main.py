import requests
import json
from twilio.rest import Client
import os

auth_token = os.environ.get("TWILIO_TOKEN")
account_sid = ""
client = Client(account_sid, auth_token)

MY_LAT = 
MY_LONG = 
API_KEY = os.environ.get("WEATHER_API")
parameters = {
    "lat":MY_LAT ,
    "lon":MY_LONG ,
    "exclude": "current,minutely,daily",
    "appid": API_KEY,
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
data = response.json()

file = open("data.json", "w")
json.dump(data, file, indent=4)
file.close()

umbrella = False
for n in range(0,12):
    id = data["hourly"][n]["weather"][0]["id"]
    if id < 600:
        umbrella = True

if umbrella == True:
    print("bring umbrella")
    message = client.messages \
                .create(
                     body="Bring an umbrella",
                     from_='+',
                     to='+'
                 )
    print(message.status)
else:
    print("Don't need umbrella today")

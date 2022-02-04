import requests
import json
from twilio.rest import Client
import os

auth_token = os.environ.get("TWILIO_TOKEN")
account_sid = "AC5f0fb9800e496e154c54467a73f53c64"
client = Client(account_sid, auth_token)

MY_LAT = 32.776665
MY_LONG = -96.796989
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
                     from_='+19792726617',
                     to='+12144177306'
                 )
    print(message.status)
else:
    print("Don't need umbrella today")

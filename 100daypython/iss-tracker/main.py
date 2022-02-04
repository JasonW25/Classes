import requests
import datetime as dt

MY_LAT = 32.776665
MY_LONG = -96.796989

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data_iss = response.json()

iss_lat = float(data_iss["iss_position"]["latitude"])
iss_long = float(data_iss["iss_position"]["longitude"])

lat_dif = MY_LAT - iss_lat
long_dif = MY_LONG - iss_long

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]
sunrise_time = sunrise.split("T")[1].split(":")[0]
sunset_time = sunset.split("T")[1].split(":")[0]
current_utc = dt.datetime.utcnow()
utc_time = str(current_utc).split(" ")[1].split(":")[0]

print(long_dif)
print(lat_dif)

if sunrise_time > utc_time or sunset_time < utc_time:
    print("night")

if -5 < lat_dif < 5 and -5 < long_dif < 5:
    if sunrise_time > utc_time or sunset_time < utc_time:
        print("You can see iss")
else:
    print("You can not see iss")
from requests.models import Response
from twilio.rest import Client
import requests
import json
import datetime as dt

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API = ""
NEWS_API = ""

auth_token = ""
account_sid = ""
data_stock = {}
message = ""

now = dt.datetime.now()
now_time = str(now).split(" ")[1].split(":")
if int(now_time[0]) >= 16:
    date = f"{now.year}-{now.month}-{now.day}"
else:
    now -= dt.timedelta(days=1)
    date = f"{now.year}-{now.month}-{now.day}"


client = Client(account_sid, auth_token)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
av_params = {
    "function":"TIME_SERIES_INTRADAY",
    "symbol":STOCK,
    "Slice":"year1month1",
    "datatype":"json",
    "interval":"60min",
    "apikey": ALPHA_API
}

# response = requests.get("https://www.alphavantage.co/query", params=av_params)
# data_stock = response.json()

# file = open("stock_data.json", "w")
# json.dump(data_stock, file, indent=4)
# file.close()

file = open("stock_data.json", "r")
data_stock = json.load(file)
file.close()
try:
    open_price = float(data_stock["Time Series (60min)"][f"{date} 09:00:00"]["1. open"])
    close_price = float(data_stock["Time Series (60min)"][f"{date} 16:00:00"]["4. close"])
except KeyError:
    try:
        now -= dt.timedelta(days=2)
        date = f"{now.year}-{now.month}-{now.day}"
        open_price = float(data_stock["Time Series (60min)"][f"{date} 09:00:00"]["1. open"])
        close_price = float(data_stock["Time Series (60min)"][f"{date} 16:00:00"]["4. close"])
    except KeyError:
        now -= dt.timedelta(days=3)
        date = f"{now.year}-{now.month}-{now.day}"
        open_price = float(data_stock["Time Series (60min)"][f"{date} 09:00:00"]["1. open"])
        close_price = float(data_stock["Time Series (60min)"][f"{date} 16:00:00"]["4. close"])



stock_change = round(((close_price - open_price) / open_price)*100, 2)
print(open_price)
print(close_price)
print(stock_change)

get_news = False
if -5 >= stock_change or stock_change >= 5:
    get_news = True

message = f"Tesla stock change: {stock_change}%\n\n"
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

get_news = True
if get_news == True:
    news_parameters = {
        "q": "Tesla",
        "from": date,
        "sortBy": "popularity",
        "apiKey": NEWS_API
    }

    # response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
    # data_news = response.json()

    # file = open("news_data.json", "w")
    # json.dump(data_news, file, indent=4)
    # file.close()

    file = open("news_data.json", "r")
    data_news = json.load(file)
    file.close()
    article_num = 0
    for article in data_news["articles"]:
        article_num += 1
        if article_num < 4:
            message += f"{article['title']}\n{article['author']}\n{article['url']}\n{article['content']}\n\n"

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

if get_news == True:
    message = client.messages \
                    .create(
                        body=message,
                        from_='+',
                        to='+'
                    )
    print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


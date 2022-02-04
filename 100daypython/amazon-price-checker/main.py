import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

price_point = 200
item_url = "https://www.amazon.com/Instant-Pot-Pressure-Steamer-Sterilizer/dp/B08PQ2KWHS/ref=sr_1_4?crid=3TNFGNUNVU83X&keywords=instant%2Bpot&qid=1642036296&s=home-garden&sprefix=insta%2Cgarden%2C237&sr=1-4&th=1"
headers = {
    "Request Line": "GET / HTTP/1.1",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4707.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

response = requests.get(item_url, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

price_rough = soup.find(name="span", class_="a-offscreen")
price = price_rough.getText().strip("$")

if price_point > float(price):
    print("hi")
    my_email = "JasonCodingTest@gmail.com"

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password="Testpassword250")
    connection.sendmail(from_addr=my_email, to_addrs="jasontwebb250@gmail.com", msg="Subject:Price Check\n\n" + f"The instapot is under {price_point} and is {price}.\n{item_url}")
    connection.close()

from twilio.rest import Client
import requests
import smtplib

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self) -> None:
        self.auth_token = "7289826a2db4e05489eb932cf398d75a"
        self.account_sid = "AC5f0fb9800e496e154c54467a73f53c64"
        self.sheety_endpoint = "https://api.sheety.co/178b21c86acd124f8b551671aa235d53/flightUsers/sheet1"
        self.token = "fn23frf823f8jd9kck3hfcevg7383df"

    def send_message(self, text):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages \
                    .create(
                        body=text,
                        from_='+19792726617',
                        to='+12144177306'
                    )
        print(message.status)

    def email(self, body):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url=self.sheety_endpoint, headers = headers)
        data = response.json()["sheet1"]
        for item in data:
            email_text = f"Hello {item['firstName']} {item['lastName']},\nHere are your flight deals:\n\n{body}"
            my_email = "JasonCodingTest@gmail.com"
            bday_email_address = item["email"]

            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(user=my_email, password="Testpassword250")
            connection.sendmail(from_addr=my_email, to_addrs=bday_email_address, msg="Subject:Flight Deals\n\n" + email_text)
            connection.close()



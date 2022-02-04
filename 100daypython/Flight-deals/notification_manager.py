from twilio.rest import Client
import requests
import smtplib

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self) -> None:
        self.auth_token = ""
        self.account_sid = ""
        self.sheety_endpoint = ""
        self.token = ""

    def send_message(self, text):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages \
                    .create(
                        body=text,
                        from_='',
                        to=''
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
            connection.login(user=my_email, password=" ")
            connection.sendmail(from_addr=my_email, to_addrs=bday_email_address, msg="Subject:Flight Deals\n\n" + email_text)
            connection.close()



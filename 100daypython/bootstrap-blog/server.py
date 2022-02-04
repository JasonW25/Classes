from concurrent.futures.process import _python_exit
from flask import Flask, render_template, request
import requests
import post
import smtplib

app = Flask(__name__)

blog_url = 'https://api.npoint.io/271adfd02f17a886e9da'
blogs = requests.get(blog_url).json()
blogs_list = []
for blog in blogs:
    item = post.Post(blog)
    blogs_list.append(item)

@app.route('/')
def home():
    return render_template("index.html", blogs=blogs_list)

@app.route('/blog/<num>')
def get_blog(num):
    global blogs_list
    return render_template('post.html', post=blogs_list[int(num)-1])

@app.route('/about')
def about():
    return render_template("about.html")
    
@app.route('/contact')
def contact():
    return render_template("contact.html", msg_sent=False)

@app.route("/form-entry", methods=["POST", "GET"])
def recieve_data():
    if request.method =="POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        my_email = "JasonCodingTest@gmail.com"
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=my_email, password="Testpassword250")
        connection.sendmail(from_addr=my_email, to_addrs=email, msg=f"Subject:From: {name}\n\n" + f"{phone}\n" + message)
        connection.close()
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

if __name__ == "__main__":
    app.run(debug=True)

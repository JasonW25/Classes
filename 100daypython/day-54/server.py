from flask import Flask
app = Flask(__name__)

# export FLASK_APP=server.py
# flask run

@app.route('/')
def hello_world():
    return 'Hello World!'

hello_world()

if __name__ == '__main__':
    app.run()


from distutils.log import debug
from flask import Flask
import random
app = Flask(__name__)

num = random.randint(0 , 9)

@app.route('/')
def index():
    return "<h3>Guess a number between 0 and 9</h3>" \
        '<iframe src="https://giphy.com/embed/3o7aCSPqXE5C6T8tBC" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/animation-retro-pixel-3o7aCSPqXE5C6T8tBC">via GIPHY</a></p>'

@app.route('/<int:number>')
def guess(number):
    global num
    if number == num:
        return "<h3>You are right!</h3>" \
            '<iframe src="https://giphy.com/embed/4T7e4DmcrP9du" width="458" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/puppy-biscuit-emerging-4T7e4DmcrP9du">via GIPHY</a></p>'
    elif number < num:
        return "<h3>Too low!</h3>" \
            '<iframe src="https://giphy.com/embed/jD4DwBtqPXRXa" width="384" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/work-digging-jD4DwBtqPXRXa">via GIPHY</a></p>'
    else:
        return "<h3>Too high!</h3>" \
            '<iframe src="https://giphy.com/embed/3o6ZtaO9BZHcOjmErm" width="480" height="453" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/dog-puppy-fly-3o6ZtaO9BZHcOjmErm">via GIPHY</a></p>'


index()

if __name__ == '__main__':
    app.run(debug=True)

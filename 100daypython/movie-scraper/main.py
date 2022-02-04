from bs4 import BeautifulSoup
import requests

response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")

soup = BeautifulSoup(response.text, "html.parser")

art_tag = soup.find_all(name='h3', class_='title')
data = [item.getText() for item in art_tag]
list = ""
for n in range(0, 100):
    name = data[n].split(")")
    try:
        item = f"{n+1}){name[1]}\n"
    except IndexError:
        name = data[n].split(":")
        item = f"{n+1}){name[1]}\n"
    list += item


with open ("list.txt", "w") as file:
    file.write(list)
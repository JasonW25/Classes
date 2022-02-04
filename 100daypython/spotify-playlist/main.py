from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

year_input = input("What date do you want a top 100 playlist from? YYYY-MM-DD format:\n")

url = f"https://www.billboard.com/charts/hot-100/{year_input}/"
CLIENT_ID = "
CLIENT_SECRET = 

response = requests.get(url)

soup = BeautifulSoup(response.text , "html.parser")
layer1 = soup.find_all(name="h3", class_="a-no-trucate")
list = [item.getText().strip() for item in layer1]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
       redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
        )
    )

user_id = sp.current_user()["id"]
print(user_id)
track_list = []
for item in list:
    year = year_input.split("-")[0]
    result = sp.search(q=f"track:{item} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        track_list.append(uri)
    except:
        pass

playlist = sp.user_playlist_create(
    user=user_id, 
    name=f"{year_input} Billboard 100", 
    public=False
    )

playlist_ID = playlist['id'] 

print(track_list)

sp.user_playlist_add_tracks(
    user=user_id,
    playlist_id=playlist_ID,
    tracks=track_list,
)

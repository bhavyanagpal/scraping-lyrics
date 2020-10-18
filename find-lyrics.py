import requests
import sys
import spotipy
import spotipy.util as util
#from config.config import USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRETSPOTIPY_REDIRECT_URI
from bs4 import BeautifulSoup


#for acessing private playlists
scope= 'playlist-read-private'
username = '8eia8ggl4ipbhouhun62o9y8i';

token = util.prompt_for_user_token( username,
         scope, client_id='3cb41450f466404399f3e0de3e4c89f2',
         client_secret= '51406619960a46c3a0fc8682e5152784',
         redirect_uri="http://localhost/" )

         
def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))
        artist = track['artists'][0]['name']
        name = track['name']
        song_url = '{}-{}-lyrics'.format(str(artist).strip().replace(' ', '-').replace('(','').replace(')',''),
                                     str(name).strip().replace(' ', '-').replace('(','').replace(')',''))
        print (song_url)

        request = requests.get("https://genius.com/{}".format(song_url))
        print(request.status_code)

        if request.status_code == 200:
        # BeautifulSoup library return an html code
            html_code = BeautifulSoup(request.text, features="html.parser")

        # Extract lyrics from beautifulsoup response using the correct prefix {"class": "lyrics"}
            lyrics = html_code.find("div", {"class": "lyrics"}).get_text()
            print(lyrics)

        else:
            print("Sorry, I can't find the actual song")                                 



if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print ('  total tracks', playlist['tracks']['total'])
            results = sp.playlist(playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
                

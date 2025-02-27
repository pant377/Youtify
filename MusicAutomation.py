import os
import re
import spotipy
import requests
import spotipy.util as util
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
from secret import *

scopes = ["https://www.googleapis.com/auth/youtube.readonly"] #https://www.googleapis.com/auth/analytics.readonly

def addtoplaylist(song,artist):
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    tracks = []
    track = urifinder(song,artist)
    tracks.append(track)
    if token:
        try:
            sp = spotipy.Spotify(auth=token)
            sp.user_playlist_add_tracks(username,"5g5bvBT483nKC4NKR3wG2m",tracks)
            print("Spotify add done...")
        except:
            print("Not Done Sorry ..")    

def urifinder(song,artist):
    scope = 'playlist-read-collaborative'
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(song,artist)
    response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token)
            })
    response_json = response.json()
    songs = response_json["tracks"]["items"]
    uri = songs[0]["uri"]
    return uri

def googlecrs():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "C:/Users/pantelis/Desktop/Spotify_Project/secret.json"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    saa = thename(youtube) 
    return saa

def thename(youtube):
    ftitle = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId="PLf1rT1a14dFyd59AMexc6DcEAkgincO3U")
    response = request.execute()
    for item in response["items"]:
        title = (item["snippet"]["title"]).replace(' [Official Video]','').replace(' [OFFICIAL VIDEO]','')
        ftitle.append(re.split('-',title)) 
    return ftitle
     
if __name__ == "__main__":
    saa = googlecrs()
    for i in saa:
        artist = i[0]    
        song = i[1]
        addtoplaylist(song,artist)
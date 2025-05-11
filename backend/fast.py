from typing import Union
import spotipy
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from spotifyToYT import showPlaylists, getSpotifyPlaylistID, songCopy, createPlaylist, songAdder
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build



load_dotenv()
app = FastAPI()

#Spotify Scopes
auth_manager=SpotifyOAuth(
            client_id= os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret= os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri= os.getenv('SPOTIFY_REDIRECT_URI'),
            scope = "user-library-read user-read-currently-playing playlist-read-private playlist-modify-public playlist-modify-private user-read-private", 
            show_dialog=True,
            cache_path= None
        )


sp = spotipy.Spotify(auth_manager=auth_manager)

#YT Scope
scopes = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/youtube'
]

YT_CLIENT_SECRET_PATH = os.getenv("YT_CLIENT_SECRET_PATH")
YT_REDIRECT_URI = os.getenv("YT_REDIRECT_URI")

#Handles Spotify oAuth fully
@app.get("/loginToSpotify")
def spAuthLink():
     authorizationURL = auth_manager.get_authorize_url(state=None)
     return authorizationURL


@app.get("/spCallback")
def spRedirectLink(code: str):
    tokenInfo = auth_manager.get_access_token(code)
    refreshedTokenInfo = auth_manager.refresh_access_token(tokenInfo['refresh_token'])
    return { "status": "Login successful" } 



#Handles YouTube oAUth fully
@app.get("/loginToYouTube")
def YTAuthLink():
     flow = InstalledAppFlow.from_client_secrets_file(
    YT_CLIENT_SECRET_PATH, 
    scopes = scopes,
    redirect_uri=YT_REDIRECT_URI
     )
     auth_url, _ = flow.authorization_url(prompt='consent')
     return RedirectResponse(auth_url)

     
     
@app.get("/ytCallback")
def YTRedirectLink(code: str):
     flow = InstalledAppFlow.from_client_secrets_file(
    YT_CLIENT_SECRET_PATH, 
    scopes = scopes,
    redirect_uri=YT_REDIRECT_URI
     )
     flow.fetch_token(code=code)
     global ytCredentials 
     ytCredentials= flow.credentials

     return {"Message" : "Auth Complete"}



#Handles going to spotify, and asking it to display it's playlists   
@app.get("/getSpotifyPlaylists")
def spotifyPlaylistGetter():
     userPlaylists = showPlaylists(sp)
     return {"User's Playlists" : userPlaylists}


#this lets user select playlists, then when they hit a convert button, converts all the spotify playlists to youtube playlists
@app.post("/convertPlaylists")
def bulkConvert(playlists: list[str]):
    global ytCredentials
    service = build('youtube', 'v3', credentials=ytCredentials)
    

    for playlistName in playlists:
        playlistID = getSpotifyPlaylistID(playlistName, sp)
        if not playlistID:
            continue

        songArray = songCopy(playlistID, sp)
        ytPlaylistId = createPlaylist(service, playlistName)
        songAdder(songArray, service, ytPlaylistId)


    return {"message": "Conversion Finished!"}






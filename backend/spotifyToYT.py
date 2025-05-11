import json
import time


def jprint(obj):  
    text = json.dumps(obj, sort_keys=True, indent=4) 
    print(text) 


#Goes to the user, returns all the playlists, and adds it into the allPlaylists var
def fetchSpPlaylists(sp):
   allSpotifyPlaylists = sp.current_user_playlists()["items"]
   return allSpotifyPlaylists



def getSpotifyPlaylistID(name: str, sp):
    userPlaylists = fetchSpPlaylists(sp)
    for playlist in userPlaylists:
        playlistName: str = playlist["name"]
    
        if playlistName.lower() == name.lower():
            return playlist["id"]
        
    return None


#Return the playlist names and ids (only show playlist names to user, then give them the option to select one of the playlists to transfer over)
def showPlaylists(sp):
    userPlaylists = fetchSpPlaylists(sp)
    playlistName = []

    for playlist in userPlaylists:
     playlistName.append(playlist["name"])

    return playlistName


#After selecting the playlist, copy the songs
def songCopy(id: str, sp):
    songArray = []
    results = sp.user_playlist_tracks(playlist_id=id)


    while results:
     for item in results["items"]:
        
        track_name = item["track"]["name"]
        songArray.append(track_name)

     if results["next"]:
        results = sp.next(results)
     else:
        break
     
    return songArray


#Go to YouTube, create a new playlist
def createPlaylist(service, name:str):
    request = service.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
            "title": name,
            "defaultLanguage": "en"
        },
        "status": {
            "privacyStatus": "private"
        }
        }
    )
    response = request.execute()
    return response["id"]

    

#Search for a song and get the id
def songSearcher(song, service):
    
    try:
        request = service.search().list(
        part="snippet",
        maxResults=1,
        q= song,
        type="video"
    )
        response = request.execute()
        items = response["items"]
    
        songId: str = items[0]["id"]["videoId"] #For now, just retrieve the first search result and extract id [quota issue]
        return songId  
    except:
        return None

    
#Add song to the playlist
def songAdder(songArray: list[str], service, ytPlaylistId: str):
      for song in songArray:
          vidID = songSearcher(song, service)

          if vidID is None: 
            continue
          
          else:
           request = service.playlistItems().insert(
           part="snippet",
           body={
            "snippet": {
            "playlistId": ytPlaylistId,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": vidID
            }
          }
        } )
          
          request.execute()
          time.sleep(0.5) 
        
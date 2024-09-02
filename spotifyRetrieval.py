import spotipy
from spotipy.oauth2 import SpotifyOAuth
from creds import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI 

from datetime import datetime

# Update the scope to include 'user-read-recently-played'




def spotifyRetrieval():
    tracks = []
    scope = 'user-read-recently-played'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

    results = sp.current_user_recently_played(limit=1)


    for item in results['items']:
        track = item['track']
        played_at = item['played_at']
        
        track = (track['name'],track['artists'][0]['name'], played_at)
        
        tracks.append(track)

    return tracks

        

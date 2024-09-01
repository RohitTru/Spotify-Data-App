import spotipy
from spotipy.oauth2 import SpotifyOAuth
from creds import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI  
import json
from datetime import datetime, timedelta
import pytz

# Update the scope to include 'user-read-recently-played'
scope = 'user-read-recently-played'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

# Get the current user's recently played tracks
results = sp.current_user_recently_played(limit=1)

# Define your local timezone, e.g., 'US/Eastern' for Eastern Time
local_tz = pytz.timezone('US/Eastern')

# Print the track information
for item in results['items']:
    track = item['track']
    # Parse the UTC time
    played_at_utc = datetime.strptime(item['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    
    # Localize the UTC time to make it timezone-aware
    played_at_utc = pytz.utc.localize(played_at_utc)
    
    # Convert to local time considering DST
    played_at_local = played_at_utc.astimezone(local_tz)
    
    # Manually adjust the time if it is still ahead by 1 hour
    played_at_local_adjusted = played_at_local - timedelta(hours=1)
    
    print(f"Track: {track['name']} - Artist: {track['artists'][0]['name']} - Played at: {played_at_local_adjusted}")

    # Save the data to a JSON file
    with open("spotify_tracks.json", "a") as f:
        json.dump({"track_name": track['name'], "artist": track['artists'][0]['name'], "played_at": str(played_at_local_adjusted)}, f)
        f.write("\n")

import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from creds import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI 

class SpotifyDatabase:
    
    def __init__(self, filename):
        """Initialize the database connection."""
        self.databaseName = filename
        self.create_sqlite_database()

    def create_sqlite_database(self):
        """Create a database connection to an SQLite database."""
        try:
            conn = sqlite3.connect(self.databaseName)
            print(f"SQLite Version: {sqlite3.sqlite_version}")
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_table(self):
        """Create the spotifyData table."""
        conn = sqlite3.connect(self.databaseName)
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS spotifyData (
                     track_Name TEXT,
                     artist TEXT,
                     time_Played TEXT
                     )""")
        conn.commit()
        conn.close()

    def insert_into_spotify_database(self, trackName, artist, timeStamp):
        """Insert data into the spotifyData table."""
        conn = sqlite3.connect(self.databaseName)
        c = conn.cursor()

        c.execute("INSERT INTO spotifyData (track_Name, artist, time_Played) VALUES (?, ?, ?)", 
                  (trackName, artist, timeStamp))
        conn.commit()
        conn.close()

    def retrieve_from_db(self):
        """Retrieve data from the spotifyData table."""
        conn = sqlite3.connect(self.databaseName)
        c = conn.cursor()

        c.execute("SELECT * FROM spotifyData")
        data = c.fetchall()

        conn.close()
        return data



tracks = []
def spotifyRetrieval(limit):
    
    scope = 'user-read-recently-played'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

    results = sp.current_user_recently_played(limit)


    for item in results['items']:
        track = item['track']
        played_at = item['played_at']
        
        track = (track['name'],track['artists'][0]['name'], played_at)
        
        tracks.append(track)

    return tracks





if __name__ == '__main__':
 
    db = SpotifyDatabase("spotifyData.db")
    db.create_table()
    db.insert_into_spotify_database('dangerous', '21 Savage', '2024-08-31 22:25:52.645000-04:00')
    data = db.retrieve_from_db()
    print(data)

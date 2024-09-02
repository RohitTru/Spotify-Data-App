import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from creds import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import time

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

    def insert_entry_into_spotify_database(self, trackName, artist, timeStamp):
        """Insert data into the spotifyData table."""
        conn = sqlite3.connect(self.databaseName)
        c = conn.cursor()

        c.execute("INSERT INTO spotifyData(track_Name, artist, time_Played) VALUES (?, ?, ?)", 
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
def spotify_Retrieval(limit):
    # Returns Spotify track details as a list of tuples
    scope = 'user-read-recently-played'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

    results = sp.current_user_recently_played(limit)


    for item in results['items']:
        track = item['track']
        playedAt = item['played_at']
        
        track = (track['name'],track['artists'][0]['name'], playedAt)
        
        tracks.append(track)

    return tracks

def update_Database():
    for i in tracks:

        db.insert_entry_into_spotify_database(i[0],i[1],i[2]) 
        
        


if __name__ == '__main__':
 
    # Creates a sqlite Data base and initialized a table to hold our table
    db = SpotifyDatabase("spotifyData.db")
    db.create_table()
    
    # Retrieve Data from spotify and store it into the database every hour
    while True:
        spotify_Retrieval(40)
        update_Database()
        time.sleep(3600)

    


    print(f'This is the data stored in the database {db.retrieve_from_db()}')
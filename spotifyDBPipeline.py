import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time
from datetime import datetime
import os

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

        # Print each entry with a newline break
        for entry in data:
            print(entry)
            print()  # This adds a newline break between each entry


    def count_duplicates(self):
        """Count the number of duplicate records based on the 'time_Played' field."""
        conn = sqlite3.connect(self.databaseName)
        c = conn.cursor()

        # Query to find duplicates
        query = """
        SELECT SUM(num_duplicates) - COUNT(*) as total_duplicates
        FROM (
            SELECT time_Played, COUNT(*) as num_duplicates
            FROM spotifyData
            GROUP BY time_Played
            HAVING COUNT(*) > 1
        );
        """
        
        c.execute(query)
        total_duplicates = c.fetchone()[0]
        c.close()
        
        return total_duplicates 
        

    
    def delete_duplicates(self):
        
        # Connect to the database
        conn = sqlite3.connect(self.databaseName)
        c = conn.cursor()

        # Find duplicates based on the unique column
        # This query selects the row ID of duplicates, except for the first occurrence
        delete_query = f"""
        DELETE FROM spotifyData
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM spotifyData
            GROUP BY time_Played
        );
        """

        try:
            
            
            
            # Execute the delete query
            c.execute(delete_query)
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the connection
            conn.close()
        
    def count_rows_in_table(self):
        conn = sqlite3.connect(self.databaseName)
        c = conn.cursor()

        c.execute(f"SELECT COUNT(*) FROM spotifyData")
        count = c.fetchone()[0]
        c.close
        return count        




def spotify_Retrieval(limit,CLIENT_ID, CLIENT_SECRET, REDIRECT_URI):

    tracks = []

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


    for i in tracks:

        db.insert_entry_into_spotify_database(i[0],i[1],i[2]) 
        




def main(db):
    
    load_dotenv()

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    

    # Retrieve Data from spotify and store it into the database every hour
    while True:
        print(f'Retrieving at {datetime.now()}')
        spotify_Retrieval(50, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    
        
        # Delete Duplicates
        print(f'{db.count_rows_in_table()} tracks in the database')
        print(f'{db.count_duplicates()} duplicates deleted based on time listened to')
        db.delete_duplicates()

        # check count again
        print(f'Updated track count: {db.count_rows_in_table()}')
       
        print('----------------------------\n\n\n')         
        time.sleep(1800)


if __name__ == '__main__':
    db = SpotifyDatabase("spotifyData.db")
    db.create_table()
    main(db)
   
    

    


   
import sqlite3

databaseName = None

# Function that creates a sqlite3 database
def create_sqlite_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    
    global databaseName 
    databaseName = str(filename)

    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        
    

# Creating our spotify data table in 
def create_Table(databaseName):
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    
    c.execute(""" CREATE TABLE spotifyData (
               track_Name,
               artist,
               time_Played
              )""")
    conn.commit()
    conn.close()

# Inserting into a table
def insert_Into_SpotifyDatabase(databaseName, trackName, artist, timeStamp):
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()

    c.execute("INSERT INTO spotifyData (track_Name, artist, time_Played) VALUES (?, ?, ?)", 
              (trackName, artist, timeStamp))
    
    conn.commit()
    conn.close()

# Retrieve from spotifyData table
def retrieveFromDB():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()

    c.execute("SELECT * FROM spotifyData")
    data = c.fetchall()

    
    conn.commit()
    conn.close()

    print(data)



if __name__ == '__main__':
    create_sqlite_database("spotifyData.db")
    create_Table(databaseName)
    insert_Into_SpotifyDatabase(databaseName,'dangerous','21 Savage','2024-08-31 22:25:52.645000-04:00')
    retrieveFromDB()
   
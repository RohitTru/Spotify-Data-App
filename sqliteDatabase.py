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

if __name__ == '__main__':
    create_sqlite_database("spotifyData.db")
   
import psycopg2

connection = psycopg2.connect("dbname=youpy_app user=youpy_user")
cursor = connection.cursor()

cursor.execute("CREATE TABLE playlists(playlistID SERIAL PRIMARY KEY, userID VARCHAR(255), name VARCHAR(255), source_platform VARCHAR(15));")
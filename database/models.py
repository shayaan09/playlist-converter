from psycopg2 import sql


#userID: Platform specific id, what each platform has given the user
USER_INFO = """
CREATE TABLE IF NOT EXISTS user(
    user_id TEXT PRIMARY KEY,
    oAuth_refresh_token TEXT NOT NULL,
    oAuth_provider VARCHAR(255) NOT NULL
);
"""


PLAYLIST_INFO = """
CREATE TABLE IF NOT EXISTS playlists(
    playlist_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    src_platform VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
"""

SONG_INFO = """
CREATE TABLE IF NOT EXISTS songs(
    song_id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL,
    artist VARCHAR(40) NOT NULL,
    track_length INTEGER
);
"""

PLATFORM_INFO = """
CREATE TABLE IF NOT EXISTS song_platform_ids(
    song_id TEXT NOT NULL,
    src_platform VARCHAR(255) NOT NULL,
    PRIMARY KEY (song_id, src_platform),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    FOREIGN KEY (src_platform) REFERENCES playlists(src_platform)
);
"""

PLAYLIST_SONGS = """
CREATE TABLE IF NOT EXISTS playlist_song(
    playlist_id TEXT NOT NULL,
    song_id TEXT NOT NULL,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
);
"""
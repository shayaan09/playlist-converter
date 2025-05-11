# Changelog

All notable changes to this project will be documented in this file.

---

## [Unreleased]

### TODO

(X) = Activity Completed

---

()Create frontend using Vite

()Change Spotify & Youtube Authorization Code Flows from local versions (only working for me) to unique for each user.

()Add logging for failed insertions and show the user the songs the program couldn't find

()Refine search algorithm - Check for artist before adding. As of 23 APR 2025: Adds songs with the same names sometimes but different artist

()Don't do fuzzy matching - Do lyrics-based searching usinf FAISS

(X)FastAPI for frontend connection with backend

()Added support for multiple platforms [Spotify <--> YouTube <--> Apple Music]

()Currently, sp and ytCredentials in fast.py are GLOBAL and will break with multiple users. Modify it.

(X)Create a database schema and start practicing postgreSQL

---

## [v1.1.3] - 2025-05-10

### Added

- Documents folder along with starting files. Learnt basic CRUD, initializations, among other things. Going to learn PostgreSQL for the database portion of this project

---

## [v1.1.3] - 2025-04-29

### Added

- `/convertPlaylists` route to support conversion of multiple Spotify playlists in one request
- Frontend can now send a list of playlist names (from checkbox selection prob) and convert all of them in one go
- YouTube playlist names now match Spotify playlist names exactly when its made

### Removed

- `/spToYouTube` route (single playlist conversion — I have bulk convert now so no need anymore)
- `/createPlaylist` route — I have bulk convert now so no need anymore
- `/playlistSelected` route — I have bulk convert now so no need anymore

---

## [v1.1.2] - 2025-04-27 + 2025-04-28

### Added

- YouTube OAuth flow (/loginToYouTube, /ytCallback)
- Used google_auth_oauthlib.flow and googleapiclient.discovery to build service object
- Stored YouTube credentials in ytCredentials global variable
- Created helper functions: createPlaylist(service, name), songSearcher(song, service), and songAdder(songArray, service, ytPlaylistId)

### Changed

- Major refactor: all functions in spotifytoYT have been implemented as "true backend" now. Were made for a CLI before
- songAdder() uses a cleaner insert flow and skips tracks without search results
- Created a working flow to create a playlist and add tracks by name

---

## [v1.1.1] - 2025-04-24

### Added

- Set up FastAPI app and environment with .env support
- Integrated SpotifyOAuth via Spotipy
- Added /loginToSpotify and /spCallback for Spotify authentication
- Created global sp instance for accessing Spotify Web API

---

## [v1.1.0] - 2025-04-21

### Added

- Error check for the videos
- Handled Pagination in songCopy()
- Added time module
- Sleep between each call to avoid the YouTube API crashing everytime

### Changed

- `songAdder` now avoids double API calls by storing YouTube video ID in a variable
- Added check to skip songs with no YouTube result (`songSearcher` returns `None`)
- Improved error messaging for missing search results
- Removed "position: 0". Was causing songs to show up in reverse order

### Fixed

- Logic bug comparing video ID to `songArray` (now removed)

---

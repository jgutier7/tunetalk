import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote

app = Flask(__name__)

# Client Keys
CLIENT_ID = "df1ec78833314c51b9a04a52ae42c2bc"
CLIENT_SECRET = "ad12172f6e824b5a95a0ce2d08cc6b5e"

# Spotify URLs
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 9152
REDIRECT_URI = "{}:{}/spotify/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# def create_spotify_client():
#     client_id = 'df1ec78833314c51b9a04a52ae42c2bc'
#     client_secret = 'ad12172f6e824b5a95a0ce2d08cc6b5e'
#     # redirect_uri = 'http://129.74.152.125:9152/spotify/callback'
#     redirect_uri = 'http://localhost:9152/spotify/callback'
#     auth_manager = SpotifyOAuth(
#         client_id=client_id,
#         client_secret=client_secret,
#         redirect_uri=redirect_uri,
#         scope='user-read-currently-playing'
#     )

#     return spotipy.Spotify(auth_manager=auth_manager)

# spotify_client = create_spotify_client()


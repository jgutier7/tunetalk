import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_client():
    client_id = 'df1ec78833314c51b9a04a52ae42c2bc'
    client_secret = 'ad12172f6e824b5a95a0ce2d08cc6b5e'
    redirect_uri = 'http://localhost:9152/spotify/callback' 

    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='user-read-currently-playing'
    )

    return spotipy.Spotify(auth_manager=auth_manager)

spotify_client = create_spotify_client()

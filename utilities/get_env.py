import os, spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

def discord_token():
    return os.getenv('DISCORD_TOKEN')

def owner_id():
    return os.getenv('OWNER_ID')

def spotify_credentials():
    return SpotifyClientCredentials(client_id=os.getenv("SPOTIPY_ID"), client_secret=os.getenv("SPOTIPY_SECRET"))

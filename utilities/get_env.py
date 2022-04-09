import os
from dotenv import load_dotenv

load_dotenv()

def discord_token():
    return os.getenv('DISCORD_TOKEN')
def discord_dev():
    return os.getenv('DISCORD_DEV')
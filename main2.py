#!/mnt/HDD500/dailymotion-sdk-python/env/bin/python
# main2.py

import os
import requests
import dailymotion
import sys
import argparse
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
d = dailymotion.Dailymotion()
d.timeout = 120  # Set a higher timeout (120 seconds)

# Fetch credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def access_token():
    """Fetches and returns an access token from Dailymotion."""
    TOKEN_URL = "https://api.dailymotion.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    response = requests.post(TOKEN_URL, data=payload)
    data = response.json()
    
    if "access_token" in data:
        logging.info("Access Token retrieved successfully.")
        return data["access_token"]
    
    logging.error("Failed to retrieve access token: %s", data)
    sys.exit(1)

def main(video_path, title, tags):
    """Uploads a video to Dailymotion."""
    
    # Check if video file exists
    if not os.path.exists(video_path):
        logging.error("File not found: %s", video_path)
        sys.exit(2)
    
    ACCESS_TOKEN = access_token()

    # Initialize Dailymotion API client
    d = dailymotion.Dailymotion()
    try:
        d.set_grant_type(
            'password',
            api_key=CLIENT_ID,
            api_secret=CLIENT_SECRET,
            scope=['read', 'write'],
            info={'username': USERNAME, 'password': PASSWORD}
        )
        d.token = ACCESS_TOKEN
        logging.info("Dailymotion API authentication successful.")

    except Exception as e:
        logging.error("Error authenticating with Dailymotion: %s", str(e))
        sys.exit(3)

    try:
        logging.info("Uploading video: %s", video_path)
        upload_url = d.upload(video_path)

        if not upload_url:
            logging.error("Video upload failed. No URL returned.")
            sys.exit(4)

        logging.info("Upload successful. URL: %s", upload_url)

        result = d.post('/me/videos', {
            'url': upload_url,
            'title': title,
            'tags': tags,
            'published': 'true',  
            'private': 'false',   
            'is_created_for_kids': 'false'
        })

        video_id = result.get('id')  # ✅ Corrected placement

        if video_id:
            update_result = d.post(f'/video/{video_id}', {'published': 'true', 'private': 'false'})
            logging.info("Video visibility updated: %s", update_result)

        logging.info("Video successfully uploaded: %s", result)

    except Exception as e:
        logging.error("Error uploading video: %s", str(e))
        sys.exit(5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Upload a video to Dailymotion.")
    parser.add_argument("--video", required=True, help="Path to the video file (.mp4)")
    parser.add_argument("--title", required=True, help="Title of the video")
    parser.add_argument("--tags", required=True, help="Comma-separated tags for the video")
    
    args = parser.parse_args()
    main(args.video, args.title, args.tags)

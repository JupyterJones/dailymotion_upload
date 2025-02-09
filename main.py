#!/mnt/HDD500/dailymotion-sdk-python/env/bin/python
import requests
import dailymotion
import sys
import argparse
from KEY import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD  # Import credentials from KEY.py

def access_token():
    TOKEN_URL = "https://api.dailymotion.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    data = response.json()
    if "access_token" in data:
        print("Access Token:", data["access_token"])
    else:
        print("Error:", data)
        sys.exit(1)
    return data["access_token"]

def main(video_path, title, tags):
    ACCESS_TOKEN = access_token()

    d = dailymotion.Dailymotion()
    d.set_grant_type(
        'password',
        api_key=CLIENT_ID,
        api_secret=CLIENT_SECRET,
        scope=['read', 'write'],
        info={'username': USERNAME, 'password': PASSWORD}
    )
    d.token = ACCESS_TOKEN

    try:
        url = d.upload(video_path)
        result = d.post('/me/videos', {
            'url': url,
            'title': title,
            'tags': tags,
            'published': 'true',
            'is_created_for_kids': 'false'
        })
        print("Video uploaded successfully:", result)

    except Exception as e:
        print("Error uploading video:", str(e))
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Upload a video to Dailymotion.")
    parser.add_argument("--video", required=True, help="Path to the video file (.mp4)")
    parser.add_argument("--title", required=True, help="Title of the video")
    parser.add_argument("--tags", required=True, help="Comma-separated tags for the video")
    args = parser.parse_args()
    main(args.video, args.title, args.tags)
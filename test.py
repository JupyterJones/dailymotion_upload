"""import requests
ACCESS_TOKEN = "OXNoSUNqHkF3ejoqVh4zPnwjPlBYUgtXGXAWRw"
# Check authentication
url = "https://api.dailymotion.com/auth"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
"""
import requests
import sys

# ----------------------
# CONFIGURATION
# ----------------------
ACCESS_TOKEN = "OXNoSUNqHkF3ejoqVh4zPnwjPlBYUgtXGXAWRw"  # Replace with your actual access token
VIDEO_PATH = 'examples/forward.mp4'  # Replace with the actual video file path
VIDEO_TITLE = "My Video Test"
VIDEO_DESCRIPTION = "This is a test upload via API"
VIDEO_TAGS = "test,api,upload"
VIDEO_IS_PUBLIC = True  # Set to False for private video

# ----------------------
# STEP 1: GET UPLOAD URL
# ----------------------
def get_upload_url():
    url = "https://api.dailymotion.com/file/upload"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "upload_url" in data:
        print("[✔] Upload URL obtained!")
        return data["upload_url"]
    else:
        print("[✘] Error getting upload URL:", data)
        sys.exit(1)

# ----------------------
# STEP 2: UPLOAD VIDEO FILE
# ----------------------
def upload_video(upload_url):
    with open(VIDEO_PATH, "rb") as file:
        files = {"file": file}
        response = requests.post(upload_url, files=files)
    
    data = response.json()
    if "url" in data:
        print("[✔] Video uploaded successfully!")
        return data["url"]
    else:
        print("[✘] Upload failed:", data)
        sys.exit(1)

# ----------------------
# STEP 3: PUBLISH VIDEO
# ----------------------
def publish_video(video_url):
    publish_url = "https://api.dailymotion.com/me/videos"
    payload = {
        "url": video_url,
        "title": VIDEO_TITLE,
        "description": VIDEO_DESCRIPTION,
        "tags": VIDEO_TAGS,
        "published": "true" if VIDEO_IS_PUBLIC else "false"
    }
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    response = requests.post(publish_url, headers=headers, data=payload)
    data = response.json()

    if "id" in data:
        video_id = data["id"]
        print(f"[✔] Video published successfully! Watch it here: https://www.dailymotion.com/video/{video_id}")
    else:
        print("[✘] Publish failed:", data)
        sys.exit(1)

# ----------------------
# RUN ALL STEPS
# ----------------------
if __name__ == "__main__":
    upload_url = get_upload_url()         # Get the upload URL
    video_url = upload_video(upload_url)  # Upload the video
    publish_video(video_url)              # Publish the video

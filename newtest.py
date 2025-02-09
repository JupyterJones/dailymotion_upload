import requests
# Replace these with your actual API keys
#ACCESS_KEY = 'eDhwTF5IMHRRTDRKFX8lE0tAHxQHfVVSGzgPXg'

# Path to the video file you want to upload
VIDEO_PATH = 'examples/forward.mp4'
# Replace these with your actual credentials
ACCESS_TOKEN = 'eDhwTF5IMHRRTDRKFX8lE0tAHxQHfVVSGzgPXg'
USER_ID = 'flaskarchtitect'  # Replace with the actual user ID

# Step 1: Create a video object
create_video_url = f'https://api.dailymotion.com/user/{USER_ID}/videos'
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}
data = {
    'title': 'My First API Upload',  # Title of the video
    'tags': 'python, automation',    # Tags for the video
    'channel': 'tech',               # Channel where the video will be published
    'description': 'This is my first video uploaded via the Dailymotion API.',
    'published': 'true',             # Publish the video immediately
    'is_created_for_kids': 'false'   # Specify whether the video is intended for kids
}

response = requests.post(create_video_url, headers=headers, data=data)
if response.status_code == 200:
    video_id = response.json().get('id')
    upload_url = response.json().get('upload_url')

    print(f'Video ID: {video_id}')
    print(f'Upload URL: {upload_url}')

    # Step 2: Upload the video file
    with open(VIDEO_PATH, 'rb') as video_file:
        files = {'file': video_file}
        upload_response = requests.post(upload_url, files=files)

    if upload_response.status_code == 200:
        print('Video uploaded successfully!')
    else:
        print('Failed to upload video:', upload_response.text)
else:
    print('Failed to create video:', response.text)
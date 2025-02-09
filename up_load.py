import dailymotion

# Initialize the Dailymotion client
d = dailymotion.Dailymotion()

# Authenticate with your access token
ACCESS_TOKEN = 'd67724b93c91d121a380'
d.set_access_token(ACCESS_TOKEN)

# Step 1: Create a video object
video_data = {
    'title': 'First API Upload',
    'tags': 'api,upload',
    'channel': 'news',
    'description': 'This is the first API upload',
    'published': 'true',
    'is_created_for_kids': 'false'  # Specify whether the video is intended for kids
}

try:
    # Create the video object
    video = d.post('/me/videos', video_data)
    video_id = video['id']
    upload_url = video['upload_url']

    print(f'Video ID: {video_id}')
    print(f'Upload URL: {upload_url}')

    # Step 2: Upload the video file
    video_file_path = 'examples/forward.mp4'
    with open(video_file_path, 'rb') as video_file:
        files = {'file': video_file}
        upload_response = requests.post(upload_url, files=files)

    if upload_response.status_code == 200:
        print('Video uploaded successfully!')
    else:
        print('Failed to upload video:', upload_response.text)

except dailymotion.DailymotionApiError as e:
    print(f'API Error: {e}')
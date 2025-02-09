#!/mnt/HDD500/dailymotion-sdk-python/env/bin/python
import requests
import dailymotion
import requests_toolbelt
def access_token():
    CLIENT_ID = 'xxxxxxxxxxxxxxxx'
    CLIENT_SECRET = 'xxxxxxxxxxxxxx'
    # Dailymotion OAuth token endpoint
    TOKEN_URL = "https://api.dailymotion.com/oauth/token"
    # Payload for requesting an access token
    payload = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
    } 
    # Send a POST request to get the access token
    response = requests.post(TOKEN_URL, data=payload)
    # Parse the response JSON
    data = response.json()
    # Print the Access Token
    if "access_token" in data:
        print("Access Token:", data["access_token"])
    else:
        print("Error:", data)
    return data["access_token"]
#Access Token: eDhwTF5IMHRRTDRKFX8lE0tAHxQHfVVSGzgPXg
# Replace these with your actual credentials
CLIENT_ID = 'xxxxxxxxxxxx'
CLIENT_SECRET = 'xxxxxxxxxxxxx'
#ACCESS_TOKEN = 'xxxxxxxxxxxxxg'
ACCESS_TOKEN = access_token()
PASSWORD ="xxxxxxxxxxxxxx"
USERNAME ="xxxxxxxxxxxx" #without the @
d = dailymotion.Dailymotion()
d.set_grant_type('password', api_key=CLIENT_ID, api_secret=CLIENT_SECRET, scope=['read', 'write'], info={'username': USERNAME, 'password': PASSWORD})
d.token = ACCESS_TOKEN
d.get('/me')
# Upload a video
VIDEO = "examples/QuickZoom_Video_By_FlaskArchitect.mp4"

# Step 1: Get the URL to upload the video
url = d.upload(VIDEO)

# Step 2: Create the video on Dailymotion
result = d.post('/me/videos', {
    'url': url,
    'title': 'QuickZoom_Video_By_FlaskArchitect',
    'tags': 'QuikZoom, FlaskArchitect',
    'published': 'true'
})

# Print the result
print(result)
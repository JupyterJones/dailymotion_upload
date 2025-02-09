#!/mnt/HDD500/dailymotion-sdk-python/env/bin/python
#I get an access token > Works great with the following code:
import requests
# Replace these with your actual credentials
CLIENT_ID = 'd67724b93c91d121a380'
CLIENT_SECRET = 'a658902d2ed9d97d604f0a7e88cb6a547613d2f9'

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
#Access Token: eDhwTF5IMHRRTDRKFX8lE0tAHxQHfVVSGzgPXg
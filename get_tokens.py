import requests
import webbrowser

# ----------------------
# CONFIGURATION
# ----------------------
CLIENT_ID = 'd67724b93c91d121a380'
CLIENT_SECRET = 'a658902d2ed9d97d604f0a7e88cb6a547613d2f9' # Your Dailymotion API Key
  # Your Dailymotion API Secret
REDIRECT_URI = "https://www.dailymotion.com"  # Can be any valid URL

# Step 1: Open browser for user authorization
AUTH_URL = f"https://www.dailymotion.com/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=manage_videos"
print("Opening browser for authorization...")
webbrowser.open(AUTH_URL)

# User must copy the `code` from the redirected URL
AUTH_CODE = input("Enter the authorization code from the redirected URL: ")

# Step 2: Exchange Authorization Code for Access & Refresh Token
TOKEN_URL = "https://api.dailymotion.com/oauth/token"
payload = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": AUTH_CODE
}

response = requests.post(TOKEN_URL, data=payload)
token_data = response.json()

if "access_token" in token_data:
    print("[✔] Access Token:", token_data["access_token"])
    print("[✔] Refresh Token:", token_data["refresh_token"])
else:
    print("[✘] Failed to get tokens:", token_data)

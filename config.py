import os

CLIENT_ID = os.getenv('DM_CLIENT_ID', '[xxxxxxxx]')
CLIENT_SECRET = os.getenv('DM_CLIENT_SECRET', '[xxxxxxxx]')
USERNAME = os.getenv('DM_USERNAME', '[XXXXXXXX]')
PASSWORD = os.getenv('DM_PASSWORD', '[XXXXXXXX]')
REDIRECT_URI = os.getenv('DM_REDIRECT_URI', '[YOUR REDIRECT URI]')
VIDEO_PATH = os.getenv('DM_VIDEO_PATH')
BASE_URL = 'https://api.dailymotion.com'
OAUTH_AUTHORIZE_URL = 'https://www.dailymotion.com/oauth/authorize'
OAUTH_TOKEN_URL = 'https://api.dailymotion.com/oauth/token'

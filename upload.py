import dailymotion

d = dailymotion.Dailymotion()
API_KEY = 'xxxxxxxxxxxx'
API_SECRET = 'xxxxxxxxxx'
USERNAME = 'xxxxxxxx' # without @
PASSWORD = 'xxxxxxxxxxxxxx'


d.set_grant_type('password', api_key=API_KEY, api_secret=API_SECRET,
    scope=['manage_videos'], info={'username': USERNAME, 'password': PASSWORD})
url = d.upload('examples/forward.mp4')
d.post(f'/user/{USERNAME}/videos',
    {'url': url, 'title': 'First API Upload', 'published': 'true', 'channel': 'news', 'description': 'This is the first API upload', 'privacy': 'unlisted', 'tags': 'api,upload','is_created_for_kids': 'false', 'is_public': 'true'})
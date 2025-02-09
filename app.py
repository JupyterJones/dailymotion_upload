from flask import Flask, request, render_template, redirect, url_for, flash
import os
import dailymotion
import sys
sys.path.append('/home/jack/hidden')
from KEY import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, FLASK_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY  # Use the secret key from KEY.py

# Configuration
UPLOAD_FOLDER = 'uploads/'

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Save the uploaded file temporarily
        video_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(video_path)
        
        # Get form data
        title = request.form.get('title', 'Untitled Video')
        tags = request.form.get('tags', 'QuikZoom, FlaskArchitect')
        
        try:
            # Authenticate with Dailymotion
            d = dailymotion.Dailymotion()
            d.set_grant_type(
                'password',
                api_key=CLIENT_ID,
                api_secret=CLIENT_SECRET,
                scope=['read', 'write'],
                info={'username': USERNAME, 'password': PASSWORD}
            )
            
            # Step 1: Upload the video file
            upload_url = d.upload(video_path)
            
            # Step 2: Create the video on Dailymotion
            result = d.post('/me/videos', {
                'url': upload_url,
                'title': title,
                'tags': tags,
                'published': 'true',
                'is_created_for_kids': 'false'
            })
            
            # Clean up the temporary file
            os.remove(video_path)
            
            flash(f"Video '{title}' uploaded successfully! Video ID: {result['id']}")
            return redirect(url_for('upload_video'))
        
        except Exception as e:
            flash(f"Error uploading video: {str(e)}")
            return redirect(request.url)
    
    return render_template('upload.html')

if __name__ == '__main__':
    #make available on lan
    app.run(debug=True, host='0.0.0.0', port=5000)
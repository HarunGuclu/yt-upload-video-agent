# 🎬 YouTube Video Upload System

A Python Flask-based YouTube video upload application with Google OAuth 2.0 integration.

**Available in:** [English](#-youtube-video-upload-system) | [Türkçe](./README.md)

## 📋 Features

✅ **Google OAuth 2.0 Authentication** - Secure Google account integration
✅ **YouTube Data API v3 Integration** - Direct video upload to YouTube channel
✅ **Drag-and-Drop Support** - Easy drag-and-drop file selection interface
✅ **Video Metadata** - Add title, description, and tags
✅ **Privacy Options** - Upload as Public, Unlisted, or Private
✅ **Shorts Support** - Automatic YouTube Shorts detection (60 seconds, vertical format)
✅ **Video Format Analysis** - Automatic video resolution, duration, and aspect ratio detection
✅ **Upload Progress Tracking** - Upload progress bar with percentage
✅ **File Validation** - File type and size checking
✅ **Secure Session Management** - Session-based authentication with mandatory re-login
✅ **Turkish Interface** - Full Turkish user interface

## 🛠️ Technical Requirements

- **Python:** 3.8+
- **Web Framework:** Flask 2.3+
- **Google Libraries:** google-auth, google-auth-oauthlib, google-api-python-client
- **Video Processing:** opencv-python, ffmpeg-python
- **Other:** python-dotenv

## 📁 Project Structure

```
youtube-video-upload/
├── app.py                          # Main Flask application
├── templates/                      # HTML templates
│   ├── giris.html                  # Login page
│   ├── giris_basarili.html         # Successful login page
│   ├── video_yukle.html            # Video upload page
│   ├── sonuc.html                  # Upload result page
│   ├── gizlilik.html               # Privacy policy
│   └── hata.html                   # Error page
├── static/                         # Static files
│   ├── css/
│   │   └── stil.css                # Main stylesheet
│   └── js/
│       └── yukle.js                # Video upload JavaScript
├── uploads/                        # Temporary file folder
├── .env                            # Environment variables (SECRET)
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore file
├── requirements.txt                # Python dependencies
├── client_secret.json              # Google API keys (SECRET)
├── README.md                       # Turkish documentation
├── README_EN.md                    # English documentation
└── KURULUM.md                      # Turkish installation guide
```

## 🚀 Installation Steps

### 1️⃣ Google Cloud Platform Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 Credentials (Web Application):
   - Add to Authorized JavaScript origins: `http://localhost:5000`
   - Add to Authorized redirect URIs: `http://localhost:5000/oauth2callback`
5. Download the JSON file and save it as `client_secret.json` in the project folder

### 2️⃣ Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

1. Copy `.env.example` and rename it to `.env`:
```bash
cp .env.example .env
```

2. Edit the `.env` file and fill in the values:
```env
FLASK_SECRET_KEY=your_strong_secret_key_here
FLASK_ENV=production
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
REDIRECT_URI=http://localhost:5000/oauth2callback
YOUTUBE_API_KEY=your_youtube_api_key_here
```

> ⚠️ **Security Warning:** Never upload the `.env` file to Git. It's already protected in `.gitignore`.

### 5️⃣ Run the Application

```bash
python app.py
```

Your browser will automatically open `http://localhost:5000`.

Or manually open:
```
http://localhost:5000
```

## 📖 Usage Guide

### Step 1: Login

1. Click the "Sign in with Google" button on the home page
2. Select your Google account
3. Grant the application permission to access your YouTube channel
4. You'll see a successful login message

### Step 2: Select Video File

1. On the video upload page, select your video file
2. You can drag and drop the file or click to select
3. Supported formats: MP4, MOV, AVI, MKV, FLV, WMV, WebM
4. Maximum file size: 5GB

### Step 3: Add Video Information

1. **Video Title** (optional): Enter the video name
2. **Video Tags** (optional): Comma-separated tags
3. **Video Description** (optional): Write a detailed description

### Step 4: Choose Video Privacy Status

Determine who can see your video:

- 🌐 **Public**: Video is visible to everyone
- 🔗 **Unlisted**: Only people with the link can view it
- 🔒 **Private**: Only you and invited people can view it

### Step 5: Choose Video Type

Determine your video format:

- 🤖 **Automatic Selection** (Recommended): System analyzes your video and selects automatically
- 📺 **Normal Video**: Long-form YouTube video (horizontal format)
- ⚡ **YouTube Shorts**: Short-form video (60 seconds or less, vertical format)

**Shorts Criteria:**
- Video duration: 60 seconds or less
- Video format: Vertical (9:16 aspect ratio)

### Step 6: Upload

1. Click the "Upload" button
2. Watch the upload progress bar
3. When upload is complete, you'll see:
   - Video ID
   - Video link
   - Video type (Shorts/Normal)
   - Privacy status
   - Video analysis information (resolution, duration, aspect ratio)
4. Click "Open on YouTube" to visit your video immediately

## 🔐 Security Features

- **OAuth 2.0**: Google's secure authentication system
- **HTTPS**: HTTPS is recommended for production environments
- **.env File**: Secret keys are stored in environment variables
- **Session Encryption**: Flask sessions are securely encrypted
- **CSRF Protection**: CSRF attacks are prevented with state parameters
- **File Validation**: File type and size are validated
- **Temporary File Cleanup**: Temporary files are deleted after upload
- **Session Control**: Mandatory re-login after logout with session protection

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/giris` | GET, POST | Login page and OAuth initialization |
| `/oauth2callback` | GET | OAuth callback endpoint |
| `/video-yukle` | GET | Video upload page |
| `/upload-video` | POST | Upload video file |
| `/video-yukle-basarili` | GET | Successful login page |
| `/cikis` | GET | Logout |
| `/gizlilik` | GET | Privacy policy |

## 🐛 Troubleshooting

### "client_secret.json not found" error

- Make sure you downloaded `client_secret.json` from Google Cloud Console
- Place the file in the project's main folder

### "GOOGLE_CLIENT_ID not found" error

- Make sure you created the `.env` file
- Fill in all required variables

### "403 Forbidden" error during upload

- Check that YouTube Data API v3 is enabled in Google Cloud Console
- Verify that your credentials are correct
- Check your API quota

### Video not uploading but no error shown

- Check your internet connection
- Check the file size (max 5GB)
- Check if YouTube supports the file format

## 📚 Library Versions

```
Flask==2.3.2
google-auth==2.23.0
google-auth-oauthlib==1.0.0
google-auth-httplib2==0.1.1
google-api-python-client==2.91.0
python-dotenv==1.0.0
Werkzeug==2.3.6
opencv-python==4.8.1.78
ffmpeg-python==0.2.1
```

## 🌐 Production Environment

When running in production:

1. **Disable Debug Mode**
```python
app.run(debug=False)
```

2. **Use HTTPS**
- Use Let's Encrypt or other SSL certificate

3. **Use Gunicorn**
```bash
pip install gunicorn
gunicorn app:app
```

4. **Set Environment Variables**
```bash
export FLASK_ENV=production
export FLASK_SECRET_KEY=your_strong_key
```

5. **Use Database** (optional)
- Consider storing session data in a database

## 🎯 YouTube Shorts vs Normal Video

YouTube automatically distinguishes between Shorts and normal videos based on:

1. **Video Duration**
   - Shorts: 60 seconds or less
   - Normal: More than 60 seconds

2. **Video Format**
   - Shorts: Vertical (9:16 aspect ratio)
   - Normal: Horizontal (16:9 aspect ratio)

3. **Resolution Examples**
   - 1920×1080 → Horizontal (normal video)
   - 1080×1920 → Vertical (potential Shorts)

The system automatically analyzes your video and provides recommendations based on these criteria.

## 📞 Support and Contact

For issues or suggestions:
- Open a GitHub Issue
- Send an email

## 📄 License

Released under the MIT License.

## 🙏 Thank You

- Google for OAuth 2.0 and YouTube API
- Flask for the web framework
- Python community

---

**Created:** 2025
**Version:** 2.0.0
**Last Updated:** October 2025

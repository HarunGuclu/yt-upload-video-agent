# 🚀 YouTube Video Upload System - Step-by-Step Setup Guide

This guide covers all the steps needed to set up the YouTube Video Upload System.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google account
- Internet connection

## 🔑 STEP 1: Google Cloud Platform Setup

### 1.1 Create a Google Cloud Project

1. Open [Google Cloud Console](https://console.cloud.google.com) in your browser
2. Click on **Select a Project**
3. Click on **New Project**
4. Enter the project name: `YouTube Video Upload`
5. Click the **Create** button

### 1.2 Enable YouTube Data API v3

1. In Google Cloud Console, type `YouTube Data API` in the search box at the top right
2. Click on **YouTube Data API v3** in the results
3. Click the **Enable** button
4. Wait for the process to complete

### 1.3 Create OAuth 2.0 Credentials

1. Click on **Credentials** in the left menu
2. Click on **+ Create Credentials**
3. Select **OAuth Client ID**
4. If prompted to configure the OAuth consent screen:
   - Click on **OAuth Consent Screen**
   - Select **External** as the user type
   - Click **Create**
5. Fill in the required fields:
   - **App name:** YouTube Video Upload System
   - **User Support Email:** Your email address
6. Click **Save and Continue**

### 1.4 Configure OAuth Consent Screen

1. Click on **Add or Remove Scopes**
2. Type `youtube.upload` in the search box
3. Select `https://www.googleapis.com/auth/youtube.upload`
4. Click **Update**
5. In the **Test Users** section, click **Add Test User**
6. Add your own Google email address
7. Click **Save**

### 1.5 Create Web Application Credentials

1. Return to the **Credentials** page
2. Click **+ Create Credentials**
3. Select **OAuth Client ID**
4. Choose **Web Application** as the application type
5. Enter the name: `YouTube Video Upload Localhost`
6. Click on **Authorized JavaScript origins** and add:
   ```
   http://localhost:5000
   ```
7. Click on **Authorized redirect URIs** and add:
   ```
   http://localhost:5000/oauth2callback
   ```
8. Click **Create**
9. Click the **Download** (JSON icon) button on the right side of the popup

### 1.6 Save the JSON File

1. Open the downloaded JSON file
2. Rename the file to `client_secret.json`
3. Copy it to the project's main folder:
   ```
   C:\Users\YourUsername\Desktop\yt-load-video-agent\client_secret.json
   ```

## 🐍 STEP 2: Python Environment Setup

### 2.1 Create Virtual Environment

On Windows:
```bash
# Navigate to the project folder
cd C:\Users\YourUsername\Desktop\yt-load-video-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

On macOS / Linux:
```bash
cd ~/Desktop/yt-load-video-agent
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

The following will be installed:
- Flask: Web framework
- google-auth: Google authentication
- google-auth-oauthlib: OAuth 2.0 support
- google-api-python-client: YouTube API client
- python-dotenv: Environment variables
- opencv-python: Video processing and analysis
- ffmpeg-python: FFmpeg Python interface

## ⚙️ STEP 3: Configure Environment Variables

### 3.1 Edit .env File

1. Open the `.env` file with a text editor (VS Code, Notepad++, etc.)
2. Fill in the following values:

```env
FLASK_SECRET_KEY=youtube-video-upload-secret-key-2025
FLASK_ENV=development
GOOGLE_CLIENT_ID=<CLIENT_ID from client_secret.json>
GOOGLE_CLIENT_SECRET=<CLIENT_SECRET from client_secret.json>
REDIRECT_URI=http://localhost:5000/oauth2callback
YOUTUBE_API_KEY=<Your YouTube API Key>
```

### 3.2 Copy Values from client_secret.json

1. Open the downloaded `client_secret.json` file
2. Find the following fields:
   - `"client_id"` - Paste to GOOGLE_CLIENT_ID
   - `"client_secret"` - Paste to GOOGLE_CLIENT_SECRET

Example:
```json
{
  "installed": {
    "client_id": "123456789.apps.googleusercontent.com",
    "client_secret": "GOCSPX-1234567890abcdef",
    ...
  }
}
```

## ▶️ STEP 4: Run the Application

### 4.1 Start Flask Application

```bash
# Make sure virtual environment is active
# Then run the application
python app.py
```

If successful, the console output will look like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

### 4.2 Open in Browser

1. Open your browser
2. Type in the address bar:
   ```
   http://localhost:5000
   ```
3. You should see the login page - Success!

## ✅ STEP 5: First Test

### 5.1 Login with Google Account

1. Click the "Sign in with Google" button
2. Select your Google account
3. Grant permission to the application
4. You'll be redirected to the next page after authorization

### 5.2 Test Video Upload

1. Click "Go to Video Upload Page"
2. Select a small test video (MP4 format)
3. Add a title and description
4. Click the "Upload" button
5. You'll see the video ID when the upload completes

## 🎯 Shorts vs Normal Video

The system automatically determines if your video should be a Shorts or normal video:

**Shorts Criteria:**
- Duration: 60 seconds or less
- Format: Vertical (9:16 aspect ratio)

The system will analyze your video and provide recommendations.

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'google'"

**Solution:**
```bash
# Make sure virtual environment is active
# Then reinstall dependencies
pip install -r requirements.txt
```

### Problem: "FileNotFoundError: client_secret.json"

**Solution:**
1. Make sure `client_secret.json` is in the project's main folder
2. Check that the filename is exactly `client_secret.json`

### Problem: "KeyError: 'GOOGLE_CLIENT_ID'"

**Solution:**
1. Make sure you created the `.env` file
2. Check that all required variables are filled
3. Restart the Flask application

### Problem: "The redirect URI provided is invalid"

**Solution:**
1. Go to Google Cloud Console
2. Go to Credentials > OAuth 2.0 Client
3. Add `http://localhost:5000/oauth2callback` to Authorized redirect URIs

### Problem: 403 Forbidden - YouTube API Error

**Solution:**
1. Check that YouTube Data API is enabled
2. Check that your account is added as a test user
3. Check API quota usage (API > Quotas)

## 📝 FAQ

### Q: Can I run the application on another computer?

A: Copy the following files and edit the `.env` file:
- app.py, templates/, static/, requirements.txt
- client_secret.json (this is secret!)
- .env (update the values)

### Q: How do I deploy to production?

A: See the "Production Environment" section in README_EN.md.

### Q: Will my data be deleted if I logout?

A: Yes, all session data is deleted when you logout.

### Q: What is the maximum file size?

A: 5 GB

## 📞 Support

If you encounter problems:
1. Check the README_EN.md file
2. Review Google Cloud Console settings again
3. Read the console error message carefully
4. Check the troubleshooting section above

---

**Good luck with your setup!** 🎉

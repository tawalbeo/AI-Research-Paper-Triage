# 🚀 Quick Start Guide - FREE Version

## Get Started in 5 Minutes!

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get FREE Gemini API Key
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy your key

**✅ FREE: 1500 requests/day - No credit card needed!**

### Step 3: Set Up Google Sheets
1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable "Google Sheets API" and "Google Drive API"
4. Create Service Account → Download JSON credentials
5. Create a Google Sheet and share it with the service account email (found in JSON file)

### Step 4: Configure Environment
```bash
# Copy the template
copy .env.example .env

# Edit .env and add:
GEMINI_API_KEY=your_key_here
GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials/google_credentials.json
SHEET_NAME=Research Papers Triage
```

### Step 5: Create Credentials Folder
```bash
mkdir credentials
# Move your Google JSON file to: credentials/google_credentials.json
```

### Step 6: Run!
```bash
python main.py
```

Drop PDF files into `papers_inbox/` folder and watch the magic happen! ✨

## What You Get FREE

- ✅ 1500 AI analyses per day
- ✅ Automatic PDF processing
- ✅ Google Sheets logging
- ✅ No credit card required
- ✅ No time limits

## Troubleshooting

**"GEMINI_API_KEY is not set"**
→ Make sure you created `.env` (not `.env.example`)

**"Google credentials file not found"**
→ Check the path in your `.env` file

**"Permission denied" on Google Sheets**
→ Share the sheet with the service account email

## Need Help?

Check the full [README.md](README.md) for detailed instructions!

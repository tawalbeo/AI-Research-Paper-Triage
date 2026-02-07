# Google Sheets Service Account Credentials

## You need to place your Google Service Account JSON file here!

### Steps to get your credentials:

1. **Go to Google Cloud Console**: https://console.cloud.google.com/

2. **Create a new project** (or select existing)

3. **Enable APIs**:
   - Go to "APIs & Services" > "Enable APIs and Services"
   - Search and enable: "Google Sheets API"
   - Search and enable: "Google Drive API"

4. **Create Service Account**:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Name it (e.g., "paper-triage-bot")
   - Click "Create and Continue"
   - Grant role: "Editor" (or more restricted)
   - Click "Done"

5. **Download JSON Key**:
   - Click on the service account you created
   - Go to "Keys" tab
   - Click "Add Key" > "Create New Key"
   - Choose JSON format
   - Download the file

6. **Save the file here** as:
   `google_credentials.json`

7. **Share your Google Sheet**:
   - Open your Google Sheet
   - Click "Share"
   - Copy the service account email from the JSON file (looks like: xxx@xxx.iam.gserviceaccount.com)
   - Paste it and give "Editor" access

## When done, your file structure should be:
```
credentials/
├── README.txt (this file)
└── google_credentials.json (your downloaded file)
```

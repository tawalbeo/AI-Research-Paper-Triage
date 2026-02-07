# AI-Powered Research Paper Triage System (FREE VERSION)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gemini API](https://img.shields.io/badge/AI-Google%20Gemini-4285F4)](https://ai.google.dev/)

An automated system that monitors a folder for new PDF research papers, processes them with **Google Gemini AI (FREE)**, and outputs structured summaries to a local CSV file.

## Features

- 📁 **Automatic Monitoring**: Watches a designated folder for new PDF files
- 📄 **Text Extraction**: Extracts text from PDF research papers
- 🤖 **AI Analysis**: Uses Google Gemini AI (FREE - 1500 requests/day) to analyze papers
- 💾 **Local CSV Output**: Saves results to CSV file (no cloud setup needed!)
- 🗂️ **File Management**: Moves processed PDFs to a separate folder
- 📝 **Structured Output**: Extracts title, authors, research area, relevance score, key findings, methodology, and more

## Demo

![Demo](https://via.placeholder.com/800x400?text=Add+Your+Demo+GIF+Here)

```bash
# Quick demo
python demo.py

# Full automation
python main.py
```

## Prerequisites

- Python 3.8 or higher
- A **FREE** Google Gemini API key (1500 requests per day)
- No credit card required!
- No cloud setup needed!

## Installation

### 1. Clone or Download the Project

```bash
cd Entry_Level_Project
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Google Gemini API (FREE)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Create a new API key
5. Copy the key for use in your `.env` file

**FREE TIER**: 1500 requests per day - perfect for research paper processing!

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file with your actual values:
   ```env
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX
   GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials/google_credentials.json
   SHEET_NAME=Research Papers Triage
   ```

3. Create a `credentials` folder and place your Google credentials JSON file there:
   ```bash
   mkdir credentials
   # Move your downloaded JSON file to credentials/google_credentials.json
   ```

## Usage

### Running the System

Start the monitoring system:

```bash
python main.py
```

You should see output like:
```
======================================================================
 Research Paper Triage System
======================================================================

Monip .env.example .env
   ```

2. Edit `.env` file with your API key:
   ```env
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX
   CSV_OUTPUT_PATH=./research_papers_results.csv
   ```

That's it! No other setup required.
### Stopping the System

Press `Ctrl+C` to stop the monitoring system.

## Project Structure

```
Entry_Level_Project/
├── papers_inbox/          # Drop new PDFs here
├── papers_processed/      # Processed PDFs are moved here
├── credentials/           # Google credentials (create this)
│   └── google_credentials.json
├── main.py               # Main orchestration script
├── pdf_processor.py      # PDF text extraction
├── ai_analyzer.py        # Gemini API integration (FREE)
├── main.py               # Main orchestration script
├── demo.py               # Quick demo script
├── pdf_processor.py      # PDF text extraction
├── ai_analyzer.py        # Gemini API integration (FREE)
├── csv_writer.py         # CSV output writer
├── config.py             # Configuration loader
├── requirements.txt      # Python dependencies
├── .env.example         # Configuration template
├── .env                 # Your configuration (create from .env.example)
├── run.bat              # Windows launcher (full system)
├── run_demo.bat         # Windows launcher (demo)
├── research_papers_results.csv  # Output
======================================================================

Monitoring: ./papers_inbox
Results CSV: ./research_papers_results.csv
## Analysis Output

The system extracts the following information for each paper:

| Field | Description CSV file
|-------|-------------|
| **Timestamp** | When the paper was processed |
| **Filename** | Original PDF filename |
| **Title** | Paper title |
| **Authors** | List of authors |
| **Research Area** | Category (Data Pipelines, Distributed Systems, Hardware Acceleration, LLMs, Other) |
| **Relevance Score** | 1-10 rating for relevance to data systems optimization |
| **Key Findings** | 2-3 sentence summary of main findings |
| **Methodology** | Brief description of research methodology 

Results are saved to `research_papers_results.csv` and can be opened in Excel, Google Sheets, or any spreadsheet application.|
| **Performance Metrics** | Any benchmarks or improvements mentioned |
| **Recommended Action** | "Deep Read", "Skim", or "Archive" |

## Configuration Options

You can customize the system by editing the `.env` file:

# Optional
CSV_OUTPUT_PATH=./research_papers_results.csv
PAPERS_INBOX=./papers_inbox
PAPERS_PROCESSED=./papers_processed
GEMINI_MODEL=gemini-2
# Optional
PAPERS_INBOX=./papers_inbox
PAPERS_PROCESSED=./papers_processed
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=8192
LOG_LEVEL=INFO
```No module named 'watchdog'" or similar
- Make sure you're using the virtual environment Python
- Run: `.venv\Scripts\python.exe main.py` (Windows)
- Or activate the environment first: `.venv\Scripts\Activate.ps1`le AI Studio

### "Google credentials file not found"
- Verify the path in `GOOGLE_SHEETS_CREDENTIALS_PATH`
- Make sure the JSON file exists at that location

### "Permission denied" on Google Sheets
- Verify you've shared the sheet with the service account email
- Check that the service account has Editor permissions

### "No text extracted from PDF"
- Some PDFs are image-based (scanned documents)
- Try using OCR software first, or use a different PDF

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Consider using a virtual environment

## Logging

The system creates a `paper_triage.log` file with detailed logging information. Check this file if you encounter issues.

## Security Notes

- **Never commit** your `.env` file or Google credentials to version control
- Add these files to `.gitignore`:to version control (already in `.gitignore`)
- The `.gitignore` file protects:
  ```
  .env                    # Your API key
  *.log                   # Log files
  papers_inbox/*.pdf      # Your PDFs
  .venv/                  # Virtual environment
  ```
- Keep your API key secure
- Rotate keys periodically

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

- [ ] Add support for multiple AI providers (OpenAI, Anthropic)
- [ ] Web interface for viewing results
- [ ] Database backend (PostgreSQL)
- [ ] Batch processing mode
- [ ] Email notifications
- [ ] Docker containerization
- [ ] Citation tracking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini AI for the free API tier
- PyMuPDF for excellent PDF processing
- The open-source community

## Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for researchers drowning in papers**
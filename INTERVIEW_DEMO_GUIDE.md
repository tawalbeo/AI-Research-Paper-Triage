# DEMO GUIDE FOR JOB INTERVIEW

## Quick 5-Minute Demo

### What This Project Does
AI-powered research paper triage system that:
- Monitors a folder for PDF research papers
- Extracts text from PDFs automatically
- Analyzes papers with Google Gemini AI (FREE)
- Saves structured summaries to CSV file
- **No credit card required!**

---

## For Your Interview - Demo Script

### 1. Show the Demo (30 seconds)
```bash
python demo.py
```

This will:
- Test the AI analysis on sample text
- Show how it extracts: title, authors, research area, relevance score, key findings, methodology, metrics
- Prove the system works end-to-end

**RESULT**: You'll see a professional analysis of the "Attention Is All You Need" paper!

---

### 2. Show the Full Automation (2 minutes)

Start the monitoring system:
```bash
python main.py
```

The system will:
-  Monitor `papers_inbox/` folder
-  Wait for PDFs to be dropped in
-  Process them automatically
-  Save results to `research_papers_results.csv`
-  Move processed PDFs to `papers_processed/`

**To Demo**: Drop a PDF into the `papers_inbox` folder while the script is running!

---

### 3. Show the Results (1 minute)

Open `research_papers_results.csv` in Excel or any text editor to show:
- Timestamp
- Filename
- Title, Authors
- Research Area (Data Pipelines, Distributed Systems, Hardware Acceleration, LLMs, Other)
- Relevance Score (1-10)
- Key Findings
- Methodology
- Performance Metrics
- Recommended Action (Deep Read / Skim / Archive)

---

## Key Talking Points for Interview

### Technical Skills Demonstrated:
1. **API Integration** - Google Gemini AI (REST API)
2. **File Processing** - PDF text extraction with PyMuPDF
3. **Automation** - Folder monitoring with watchdog
4. **Data Extraction** - Structured JSON parsing from AI responses
5. **Error Handling** - Robust logging and exception handling
6. **Configuration** - Environment variables for API keys
7. **Python Best Practices** - Modular code, type hints, documentation

### Architecture:
- **Modular Design**: Separated concerns (PDF processing, AI analysis, output writing, orchestration)
- **config.py** - Centralized configuration
- **pdf_processor.py** - PDF text extraction
- **ai_analyzer.py** - AI integration with structured prompts
- **csv_writer.py** - Data persistence
- **main.py** - Orchestration and folder monitoring

### Scalability Discussion Points:
- Could easily swap CSV for database (PostgreSQL, MongoDB)
- Could add more AI providers (OpenAI, Anthropic, etc.)
- Could deploy as web service with FastAPI
- Could add email notifications
- Could process papers in parallel with multiprocessing

### Cost Consciousness:
- Used FREE Gemini API (1500 requests/day) instead of paid options
- Local CSV files instead of Google Sheets (no credit card needed)
- Lightweight dependencies

---

## If They Ask: "Why This Project?"

**Answer**: 
"I built this to solve a real problem researchers face - staying on top of new papers. It demonstrates:
- Working with modern AI APIs
- Building practical automation tools
- Clean, maintainable code architecture
- Cost-conscious engineering (using free tools)"

---

## Quick Demo Checklist

Before your interview:
- [ ] Test `python demo.py` - verify it works
- [ ] Have a PDF ready to drop into `papers_inbox/`
- [ ] Know where `research_papers_results.csv` is saved
- [ ] Be ready to explain the code architecture
- [ ] Have this demo guide open for reference

---

## Project Structure to Discuss

```
Entry_Level_Project/
├── demo.py              # Quick test script
├── main.py             # Full automation with folder monitoring
├── config.py           # Configuration management
├── pdf_processor.py    # PDF text extraction
├── ai_analyzer.py      # AI integration
├── csv_writer.py       # Results output
├── requirements.txt    # Dependencies
├── .env               # API configuration
└── papers_inbox/      # Drop PDFs here
└── papers_processed/  # Completed PDFs move here
└── research_papers_results.csv  # Output file
```

---

## Bonus: Real-World Extensions

If they ask "What would you add?":
1. **Web Interface** - Flask/FastAPI dashboard to view results
2. **Database** - PostgreSQL for better querying
3. **Email Digests** - Weekly summary of top papers
4. **Multi-language** - Support papers in different languages
5. **Citation Analysis** - Track paper citations
6. **Duplicate Detection** - Avoid processing same paper twice
7. **Batch Processing** - Process entire folders at once
8. **Cloud Deployment** - AWS Lambda or Google Cloud Functions

---

Good luck with your interview! 🚀

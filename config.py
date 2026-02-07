"""
Configuration loader for the research paper triage system.
Loads environment variables and validates required settings.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for application settings."""
    
    # API Keys and Credentials
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Output file
    CSV_OUTPUT_PATH = os.getenv('CSV_OUTPUT_PATH', str(Path(__file__).parent / 'research_papers_results.csv'))
    
    # Folder paths
    BASE_DIR = Path(__file__).parent
    PAPERS_INBOX = os.getenv('PAPERS_INBOX', str(BASE_DIR / 'papers_inbox'))
    PAPERS_PROCESSED = os.getenv('PAPERS_PROCESSED', str(BASE_DIR / 'papers_processed'))
    
    # Gemini API settings (FREE tier available!)
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '8192'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration is present."""
        errors = []
        
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is not set")
        
        # Ensure folders exist
        Path(cls.PAPERS_INBOX).mkdir(parents=True, exist_ok=True)
        Path(cls.PAPERS_PROCESSED).mkdir(parents=True, exist_ok=True)
        
        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True


# Validate configuration on import (optional - comment out if you want to handle validation elsewhere)
# Config.validate()

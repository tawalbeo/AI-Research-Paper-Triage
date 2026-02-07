"""
Google Sheets integration module.
Handles writing analysis results to Google Sheets.
"""

import logging
from datetime import datetime
from typing import Dict, Any
import gspread
from google.oauth2.service_account import Credentials
from config import Config

logger = logging.getLogger(__name__)


class SheetsWriter:
    """Handles writing data to Google Sheets."""
    
    # Required Google Sheets API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Column headers for the sheet
    HEADERS = [
        'Timestamp',
        'Filename',
        'Title',
        'Authors',
        'Research Area',
        'Relevance Score',
        'Key Findings',
        'Methodology',
        'Performance Metrics',
        'Recommended Action'
    ]
    
    def __init__(self, credentials_path: str = None, sheet_name: str = None):
        """
        Initialize the Google Sheets writer.
        
        Args:
            credentials_path: Path to Google service account JSON file
            sheet_name: Name of the Google Sheet to write to
        """
        self.credentials_path = credentials_path or Config.GOOGLE_SHEETS_CREDENTIALS_PATH
        self.sheet_name = sheet_name or Config.SHEET_NAME
        
        if not self.credentials_path:
            raise ValueError("Google Sheets credentials path is required")
        
        self.client = None
        self.sheet = None
        self.worksheet = None
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Google Sheets client and authenticate."""
        try:
            logger.info("Authenticating with Google Sheets API")
            
            # Load credentials
            creds = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            
            # Create client
            self.client = gspread.authorize(creds)
            
            # Open or create the sheet
            self._setup_sheet()
            
            logger.info(f"Successfully connected to Google Sheet: {self.sheet_name}")
            
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Google credentials file not found: {self.credentials_path}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets client: {str(e)}")
            raise Exception(f"Google Sheets authentication failed: {str(e)}")
    
    def _setup_sheet(self):
        """Open existing sheet or create a new one with headers."""
        try:
            # Try to open existing sheet
            self.sheet = self.client.open(self.sheet_name)
            self.worksheet = self.sheet.sheet1
            
            # Check if headers exist, if not, add them
            existing_headers = self.worksheet.row_values(1)
            if not existing_headers or existing_headers != self.HEADERS:
                logger.info("Adding headers to sheet")
                self.worksheet.insert_row(self.HEADERS, 1)
            
        except gspread.SpreadsheetNotFound:
            # Create new sheet if it doesn't exist
            logger.info(f"Creating new Google Sheet: {self.sheet_name}")
            self.sheet = self.client.create(self.sheet_name)
            self.worksheet = self.sheet.sheet1
            
            # Add headers
            self.worksheet.insert_row(self.HEADERS, 1)
            
            logger.info(f"Created new sheet: {self.sheet.url}")
    
    def write_analysis(self, analysis: Dict[str, Any], filename: str) -> bool:
        """
        Write analysis results to Google Sheets.
        
        Args:
            analysis: Dictionary containing analysis results from Claude
            filename: Name of the processed PDF file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Writing analysis to Google Sheets: {filename}")
            
            # Prepare row data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            row_data = [
                timestamp,
                filename,
                analysis.get('title', 'N/A'),
                analysis.get('authors', 'N/A'),
                analysis.get('research_area', 'Other'),
                analysis.get('relevance_score', 'N/A'),
                analysis.get('key_findings', 'N/A'),
                analysis.get('methodology', 'N/A'),
                analysis.get('performance_metrics', 'N/A'),
                analysis.get('recommended_action', 'N/A')
            ]
            
            # Append row to sheet
            self.worksheet.append_row(row_data)
            
            logger.info(f"Successfully wrote analysis for: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write to Google Sheets: {str(e)}")
            return False
    
    def get_sheet_url(self) -> str:
        """
        Get the URL of the Google Sheet.
        
        Returns:
            URL string
        """
        if self.sheet:
            return self.sheet.url
        return ""

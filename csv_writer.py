"""
CSV writer module - Local file alternative to Google Sheets.
Handles writing analysis results to a local CSV file.
"""

import logging
import csv
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)


class CSVWriter:
    """Handles writing data to local CSV file."""
    
    # Column headers for the CSV
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
    
    def __init__(self, csv_path: str = None):
        """
        Initialize the CSV writer.
        
        Args:
            csv_path: Path to CSV file (defaults to Config.CSV_OUTPUT_PATH)
        """
        self.csv_path = csv_path or Config.CSV_OUTPUT_PATH
        
        # Ensure the file exists with headers
        self._initialize_csv()
        
        logger.info(f"CSV Writer initialized: {self.csv_path}")
    
    def _initialize_csv(self):
        """Create CSV file with headers if it doesn't exist."""
        csv_file = Path(self.csv_path)
        
        # Create parent directory if needed
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create file with headers if it doesn't exist
        if not csv_file.exists():
            logger.info(f"Creating new CSV file: {self.csv_path}")
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.HEADERS)
    
    def write_analysis(self, analysis: Dict[str, Any], filename: str) -> bool:
        """
        Write analysis results to CSV file.
        
        Args:
            analysis: Dictionary containing analysis results from AI
            filename: Name of the processed PDF file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Writing analysis to CSV: {filename}")
            
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
            
            # Append row to CSV
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(row_data)
            
            logger.info(f"Successfully wrote analysis for: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write to CSV: {str(e)}")
            return False
    
    def get_file_path(self) -> str:
        """
        Get the full path of the CSV file.
        
        Returns:
            Path string
        """
        return str(Path(self.csv_path).absolute())

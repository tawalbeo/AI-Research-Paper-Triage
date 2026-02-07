"""
PDF text extraction module.
Handles extracting text content from PDF files using PyMuPDF.
"""

import fitz  # PyMuPDF
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles PDF text extraction."""
    
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If PDF extraction fails
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        try:
            logger.info(f"Extracting text from: {pdf_path.name}")
            
            # Open the PDF
            doc = fitz.open(pdf_path)
            
            # Extract text from all pages
            text_content = []
            page_count = len(doc)
            for page_num in range(page_count):
                page = doc[page_num]
                text = page.get_text()
                text_content.append(text)
            
            doc.close()
            
            # Join all pages with double newline
            full_text = "\n\n".join(text_content)
            
            # Log statistics
            word_count = len(full_text.split())
            logger.info(f"Extracted {page_count} pages, ~{word_count} words from {pdf_path.name}")
            
            if not full_text.strip():
                logger.warning(f"No text extracted from {pdf_path.name} - might be scanned/image-based PDF")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path.name}: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_limited(pdf_path: str, max_chars: int = 100000) -> str:
        """
        Extract text from PDF with a character limit (useful for API limits).
        
        Args:
            pdf_path: Path to the PDF file
            max_chars: Maximum number of characters to extract
            
        Returns:
            Extracted text, truncated if necessary
        """
        full_text = PDFProcessor.extract_text(pdf_path)
        
        if len(full_text) > max_chars:
            logger.warning(f"Text truncated from {len(full_text)} to {max_chars} characters")
            return full_text[:max_chars] + "\n\n[... Text truncated due to length ...]"
        
        return full_text

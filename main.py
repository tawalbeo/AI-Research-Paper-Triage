"""
Main orchestration script for the Research Paper Triage System.
Monitors folder for new PDFs, processes them with Claude AI, and outputs to Google Sheets.
"""

import time
import logging
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from config import Config
from pdf_processor import PDFProcessor
from ai_analyzer import AIAnalyzer
from csv_writer import CSVWriter


# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('paper_triage.log')
    ]
)

logger = logging.getLogger(__name__)


class PaperHandler(FileSystemEventHandler):
    """Handles file system events for new PDF files."""
    
    def __init__(self, processor: PDFProcessor, analyzer: AIAnalyzer, writer: CSVWriter):
        """
        Initialize the paper handler.
        
        Args:
            processor: PDFProcessor instance
            analyzer: AIAnalyzer instance
            writer: CSVWriter instance
        """
        self.processor = processor
        self.analyzer = analyzer
        self.writer = writer
        self.processing = set()  # Track files currently being processed
    
    def on_created(self, event: FileCreatedEvent):
        """
        Handle file creation events.
        
        Args:
            event: File system event
        """
        # Only process PDF files
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if file_path.suffix.lower() != '.pdf':
            return
        
        # Avoid processing the same file multiple times
        if str(file_path) in self.processing:
            return
        
        # Wait a moment to ensure file is fully written
        time.sleep(1)
        
        self.processing.add(str(file_path))
        
        try:
            self.process_paper(file_path)
        finally:
            self.processing.discard(str(file_path))
    
    def process_paper(self, pdf_path: Path):
        """
        Process a single research paper through the full pipeline.
        
        Args:
            pdf_path: Path to the PDF file
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing new paper: {pdf_path.name}")
        logger.info(f"{'='*60}")
        
        try:
            # Step 1: Extract text from PDF
            logger.info("Step 1/4: Extracting text from PDF...")
            paper_text = self.processor.extract_text_limited(str(pdf_path), max_chars=100000)
            
            if not paper_text.strip():
                logger.error(f"No text extracted from {pdf_path.name} - skipping")
                return
            
            # Step 2: Analyze with Gemini AI (FREE)
            logger.info("Step 2/4: Analyzing paper with Gemini AI...")
            analysis = self.analyzer.analyze_paper(paper_text, pdf_path.name)
            
            # Step 3: Write to CSV file
            logger.info("Step 3/4: Writing results to CSV file...")
            success = self.writer.write_analysis(analysis, pdf_path.name)
            
            if not success:
                logger.error("Failed to write to CSV file")
                return
            
            # Step 4: Move to processed folder
            logger.info("Step 4/4: Moving PDF to processed folder...")
            processed_path = Path(Config.PAPERS_PROCESSED) / pdf_path.name
            
            # Handle duplicate filenames
            counter = 1
            while processed_path.exists():
                stem = pdf_path.stem
                processed_path = Path(Config.PAPERS_PROCESSED) / f"{stem}_{counter}.pdf"
                counter += 1
            
            shutil.move(str(pdf_path), str(processed_path))
            
            logger.info(f"OK - Successfully processed: {pdf_path.name}")
            logger.info(f"  Title: {analysis.get('title', 'N/A')}")
            logger.info(f"  Relevance Score: {analysis.get('relevance_score', 'N/A')}/10")
            logger.info(f"  Recommendation: {analysis.get('recommended_action', 'N/A')}")
            logger.info(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path.name}: {str(e)}", exc_info=True)
            logger.info(f"{'='*60}\n")


def main():
    """Main function to run the paper triage system."""
    
    print("\n" + "="*70)
    print(" Research Paper Triage System")
    print("="*70 + "\n")
    
    try:
        # Validate configuration
        logger.info("Validating configuration...")
        Config.validate()
        logger.info("OK - Configuration validated")
        
        # Initialize components
        logger.info("\nInitializing components...")
        
        processor = PDFProcessor()
        logger.info("OK - PDF Processor initialized")
        
        analyzer = AIAnalyzer()
        logger.info("OK - AI Analyzer initialized")
        
        writer = CSVWriter()
        logger.info(f"OK - CSV Writer initialized")
        logger.info(f"  Output file: {writer.get_file_path()}")
        
        # Set up file system observer
        event_handler = PaperHandler(processor, analyzer, writer)
        observer = Observer()
        observer.schedule(event_handler, Config.PAPERS_INBOX, recursive=False)
        observer.start()
        
        logger.info(f"\nOK - Now monitoring folder: {Config.PAPERS_INBOX}")
        logger.info("  Waiting for new PDF files...")
        logger.info("  Press Ctrl+C to stop\n")
        
        print(f"Monitoring: {Config.PAPERS_INBOX}")
        print(f"Results CSV: {writer.get_file_path()}")
        print("\nDrop PDF files into the inbox folder to process them automatically.\n")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            logger.info("\n\nShutting down...")
        
        observer.join()
        logger.info("OK - Shutdown complete")
        
    except Exception as e:
        logger.error(f"\nFatal error: {str(e)}", exc_info=True)
        print(f"\nError: {str(e)}")
        print("\nPlease check your configuration and try again.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

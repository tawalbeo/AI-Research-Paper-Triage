"""
DEMO SCRIPT - Test the AI paper analysis without Google Sheets
Just processes one PDF and shows results in terminal!
"""

import sys
from pathlib import Path

# Add colored output for Windows
try:
    import colorama
    colorama.init()
except:
    pass

print("\n" + "="*70)
print(" QUICK DEMO - AI Research Paper Analyzer")
print("="*70)

# Check for Gemini API key
from config import Config
print("\n[1/4] Checking configuration...")
try:
    Config.validate()
    print("      OK - Gemini API key found!")
except ValueError as e:
    if "GEMINI_API_KEY" in str(e):
        print("      ERROR - No Gemini API key found in .env file")
        sys.exit(1)

# Initialize PDF processor
print("\n[2/4] Initializing PDF processor...")
from pdf_processor import PDFProcessor
processor = PDFProcessor()
print("      OK - PDF processor ready")

# Initialize AI analyzer
print("\n[3/4] Initializing Gemini AI...")
from ai_analyzer import AIAnalyzer
analyzer = AIAnalyzer()
print("      OK - Gemini AI ready (FREE API)")

# Look for a PDF to test
print("\n[4/4] Looking for PDF files...")
inbox_path = Path(Config.PAPERS_INBOX)
pdf_files = list(inbox_path.glob("*.pdf"))

if not pdf_files:
    print(f"\n      No PDF files found in: {inbox_path}")
    print(f"\n      Add a PDF file to '{inbox_path}' and run again!")
    print("\n" + "="*70)
    
    # Create a sample text to analyze instead
    print("\n      Testing with sample academic text instead...\n")
    
    sample_text = """
    Attention Is All You Need
    
    Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, 
    Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin
    
    Abstract: The dominant sequence transduction models are based on complex 
    recurrent or convolutional neural networks that include an encoder and a 
    decoder. The best performing models also connect the encoder and decoder 
    through an attention mechanism. We propose a new simple network architecture, 
    the Transformer, based solely on attention mechanisms, dispensing with 
    recurrence and convolutions entirely. Experiments on two machine translation 
    tasks show these models to be superior in quality while being more 
    parallelizable and requiring significantly less time to train.
    
    On the WMT 2014 English-to-German translation task, our model achieves 
    28.4 BLEU, improving over the existing best results by over 2 BLEU. On the 
    WMT 2014 English-to-French translation task, our model establishes a new 
    single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days 
    on eight GPUs, a small fraction of the training costs of the best models from 
    the literature.
    """
    
    print("      Analyzing sample text with Gemini AI...\n")
    
    try:
        analysis = analyzer.analyze_paper(sample_text, "sample_paper.pdf")
        
        print("\n" + "="*70)
        print(" ANALYSIS RESULTS")
        print("="*70)
        print(f"\nTitle: {analysis['title']}")
        print(f"\nAuthors: {analysis['authors']}")
        print(f"\nResearch Area: {analysis['research_area']}")
        print(f"\nRelevance Score: {analysis['relevance_score']}/10")
        print(f"\nKey Findings:\n{analysis['key_findings']}")
        print(f"\nMethodology:\n{analysis['methodology']}")
        print(f"\nPerformance Metrics:\n{analysis['performance_metrics']}")
        print(f"\nRecommended Action: {analysis['recommended_action']}")
        print("\n" + "="*70)
        print(" DEMO SUCCESSFUL!")
        print("="*70)
        print("\nThe system works! Add PDF files to papers_inbox/ to process them.")
        print("Set up Google Sheets credentials to save results automatically.")
        
    except Exception as e:
        print(f"\n      ERROR: {str(e)}")
        sys.exit(1)
    
else:
    # Process the first PDF found
    pdf_file = pdf_files[0]
    print(f"\n      Found: {pdf_file.name}")
    print(f"\n      Processing PDF with Gemini AI...\n")
    
    try:
        # Extract text from PDF
        print("      Extracting text from PDF...")
        text = processor.extract_text_limited(str(pdf_file), max_chars=50000)
        print(f"      Extracted ~{len(text)} characters")
        
        # Analyze with AI
        print("      Sending to Gemini AI for analysis...")
        analysis = analyzer.analyze_paper(text, pdf_file.name)
        
        # Display results
        print("\n" + "="*70)
        print(" ANALYSIS RESULTS")
        print("="*70)
        print(f"\nFilename: {pdf_file.name}")
        print(f"\nTitle: {analysis['title']}")
        print(f"\nAuthors: {analysis['authors']}")
        print(f"\nResearch Area: {analysis['research_area']}")
        print(f"\nRelevance Score: {analysis['relevance_score']}/10")
        print(f"\nKey Findings:\n{analysis['key_findings']}")
        print(f"\nMethodology:\n{analysis['methodology']}")
        print(f"\nPerformance Metrics:\n{analysis['performance_metrics']}")
        print(f"\nRecommended Action: {analysis['recommended_action']}")
        print("\n" + "="*70)
        print(" DEMO SUCCESSFUL!")
        print("="*70)
        print("\nThe system works! Set up Google Sheets to save results automatically.")
        print("Run 'python main.py' for full automation with folder monitoring.")
        
    except Exception as e:
        print(f"\n      ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

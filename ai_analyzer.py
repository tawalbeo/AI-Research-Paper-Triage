"""
AI analysis module using Google Gemini API (FREE).
Sends research paper text to Gemini and receives structured analysis.
"""

import json
import logging
import google.generativeai as genai
from typing import Dict, Any
from config import Config

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """Handles interaction with Google Gemini API for paper analysis."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the AI analyzer.
        
        Args:
            api_key: Google Gemini API key (defaults to Config.GEMINI_API_KEY)
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Google Gemini API key is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.max_tokens = Config.MAX_TOKENS
    
    def analyze_paper(self, paper_text: str, filename: str = "") -> Dict[str, Any]:
        """
        Analyze a research paper using Google Gemini API (FREE).
        
        Args:
            paper_text: The extracted text from the research paper
            filename: Optional filename for context
            
        Returns:
            Dictionary containing structured analysis results
            
        Raises:
            Exception: If API call fails or response parsing fails
        """
        try:
            logger.info(f"Sending paper to Gemini API for analysis: {filename}")
            
            # Construct the prompt
            prompt = self._build_analysis_prompt(paper_text, filename)
            
            # Call Gemini API
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=0.2,  # Lower temperature for more consistent JSON
                )
            )
            
            # Extract the response text
            response_text = response.text
            logger.debug(f"Gemini API response: {response_text}")
            
            # Parse JSON response
            analysis = self._parse_response(response_text)
            
            logger.info(f"Successfully analyzed paper: {analysis.get('title', 'Unknown')}")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {str(e)}")
            raise Exception(f"Invalid JSON response from Gemini: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error during Gemini API call: {str(e)}")
            raise Exception(f"Failed to analyze paper: {str(e)}")
    
    def _build_analysis_prompt(self, paper_text: str, filename: str = "") -> str:
        """
        Build the prompt for Gemini API.
        
        Args:
            paper_text: The research paper text
            filename: Optional filename
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert research paper analyst specializing in data systems, distributed computing, and performance optimization.

Analyze the following research paper and extract structured information. Return your analysis ONLY as a valid JSON object, with no additional text before or after.

Research Paper Text:
{paper_text}

Provide your analysis in the following JSON format:
{{
  "title": "The full title of the paper",
  "authors": "Comma-separated list of authors",
  "research_area": "One of: Data Pipelines, Distributed Systems, Hardware Acceleration, LLMs, Other",
  "relevance_score": 8,
  "key_findings": "2-3 sentences summarizing the main findings",
  "methodology": "Brief description of the research methodology",
  "performance_metrics": "Any benchmarks, speedups, or performance improvements mentioned",
  "recommended_action": "One of: Deep Read, Skim, Archive"
}}

Guidelines:
- relevance_score: Rate 1-10 based on relevance to data systems optimization research
- research_area: Choose the most appropriate category from the list
- recommended_action: 
  * "Deep Read" for highly relevant papers (score 8-10)
  * "Skim" for moderately relevant papers (score 4-7)
  * "Archive" for low relevance papers (score 1-3)
- If information is not available, use "Not specified" or "N/A"

Return ONLY the JSON object, no additional commentary."""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Gemini's response and validate the structure.
        
        Args:
            response_text: Raw response from Gemini
            
        Returns:
            Parsed and validated dictionary
            
        Raises:
            json.JSONDecodeError: If response is not valid JSON
            ValueError: If required fields are missing
        """
        # Try to find JSON in the response (in case there's extra text)
        response_text = response_text.strip()
        
        # Find JSON object boundaries
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_text = response_text[start_idx:end_idx + 1]
        else:
            json_text = response_text
        
        # Parse JSON
        analysis = json.loads(json_text)
        
        # Validate required fields
        required_fields = [
            'title', 'authors', 'research_area', 'relevance_score',
            'key_findings', 'methodology', 'performance_metrics', 'recommended_action'
        ]
        
        missing_fields = [field for field in required_fields if field not in analysis]
        if missing_fields:
            raise ValueError(f"Missing required fields in response: {missing_fields}")
        
        # Validate relevance_score is an integer between 1-10
        try:
            score = int(analysis['relevance_score'])
            if not 1 <= score <= 10:
                logger.warning(f"Relevance score {score} out of range, clamping to 1-10")
                analysis['relevance_score'] = max(1, min(10, score))
        except (ValueError, TypeError):
            logger.warning(f"Invalid relevance score, defaulting to 5")
            analysis['relevance_score'] = 5
        
        return analysis

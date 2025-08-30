"""
Local Web Reader - A cost-effective web scraping and summarization tool using Ollama

This tool provides AI-powered website analysis without API costs by using local LLM models.
Perfect for businesses looking to reduce AI infrastructure costs while maintaining functionality.

Key Benefits:
- Zero API costs after initial setup
- Complete data privacy (no external API calls)
- Customizable AI models
- Scalable for enterprise use

Author: Your Name
Model Used: Llama 3.2 (via Ollama)
Cost: $0 per request (after local setup)
"""

import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import ollama
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
DEFAULT_MODEL = "llama3.2"

class Website:
    """
    A utility class to represent a website that we have scraped.
    
    This class handles web scraping, content cleaning, and text extraction
    optimized for AI processing.
    
    Attributes:
        url (str): The website URL
        title (str): The page title
        text (str): Clean text content for AI analysis
        raw_content (str): Original HTML content
        status_code (int): HTTP response status code
    """
    
    def __init__(self, url: str, timeout: int = 10):
        """
        Create a Website object from the given URL using BeautifulSoup.
        
        Args:
            url (str): The website URL to scrape
            timeout (int): Request timeout in seconds (default: 10)
        """
        self.url = url
        self.title = ""
        self.text = ""
        self.raw_content = ""
        self.status_code = None
        
        try:
            self._scrape_website(timeout)
            logger.info(f"Successfully scraped: {self.title}")
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            self._handle_scraping_error(str(e))
    
    def _scrape_website(self, timeout: int) -> None:
        """Internal method to handle the actual web scraping."""
        response = requests.get(self.url, timeout=timeout)
        response.raise_for_status()
        self.status_code = response.status_code
        
        soup = BeautifulSoup(response.content, 'html.parser')
        self.raw_content = str(soup)
        
        # Extract title
        self.title = soup.title.string.strip() if soup.title else "No title found"
        
        # Clean content for better AI processing
        if soup.body:
            # Remove irrelevant elements
            for irrelevant in soup.body(["script", "style", "img", "input", "nav", "header", "footer"]):
                irrelevant.decompose()
            
            # Extract clean text
            self.text = soup.body.get_text(separator="\n", strip=True)
            
            # Additional cleaning
            self.text = self._clean_text(self.text)
        else:
            self.text = soup.get_text(separator="\n", strip=True)
    
    def _clean_text(self, text: str) -> str:
        """Clean and optimize text for AI processing."""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and very short lines (likely navigation)
            if len(line) > 10:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _handle_scraping_error(self, error_message: str) -> None:
        """Handle scraping errors gracefully."""
        self.title = "Error loading website"
        self.text = f"Failed to load website content: {error_message}"
        self.status_code = None


class LocalWebReader:
    """
    Main class for local AI-powered web analysis using Ollama.
    
    This class provides cost-effective web content analysis using local LLM models,
    eliminating API costs and ensuring data privacy.
    
    Business Value:
    - Cost Reduction: $0 per request vs $0.01-0.03 per request with cloud APIs
    - Data Privacy: All processing done locally
    - Customization: Full control over AI models and prompts
    - Scalability: No rate limits or usage quotas
    """
    
    def __init__(self, model: str = DEFAULT_MODEL):
        """
        Initialize the LocalWebReader with specified model.
        
        Args:
            model (str): Ollama model name (default: llama3.2)
        """
        self.model = model
        self.system_prompt = """You are an assistant that analyzes the contents of a website 
and provides a short summary, ignoring text that might be navigation related. 
Respond in markdown."""
        
        # Verify Ollama is available
        self._check_ollama_availability()
        
        logger.info(f"LocalWebReader initialized with model: {model}")
    
    def _check_ollama_availability(self) -> None:
        """Check if Ollama is running and model is available."""
        try:
            models = ollama.list()
            available_models = [model['name'] for model in models['models']]
            
            if self.model not in available_models:
                logger.warning(f"Model {self.model} not found. Available models: {available_models}")
                print(f"⚠️  Model '{self.model}' not found locally.")
                print(f"Available models: {', '.join(available_models)}")
                print(f"To install the model, run: ollama pull {self.model}")
            else:
                logger.info(f"Model {self.model} is available")
                
        except Exception as e:
            logger.error(f"Ollama connection failed: {str(e)}")
            print("❌ Ollama is not running or not accessible.")
            print("Please ensure Ollama is installed and running.")
            print("Visit: https://ollama.ai for installation instructions")
    
    def set_system_prompt(self, prompt: str) -> None:
        """
        Set a custom system prompt for AI analysis.
        
        Args:
            prompt (str): Custom system prompt
        """
        self.system_prompt = prompt
        logger.info("System prompt updated")
    
    def user_prompt_for(self, website: Website) -> str:
        """
        Generate a user prompt for website analysis.
        
        Args:
            website (Website): Website object to analyze
            
        Returns:
            str: Formatted user prompt
        """
        user_prompt = f"You are looking at a website titled '{website.title}'\n"
        user_prompt += "The contents of this website is as follows; "
        user_prompt += "please provide a short summary of this website in markdown. "
        user_prompt += "If it includes news or announcements, then summarize these too.\n\n"
        user_prompt += website.text
        return user_prompt
    
    def messages_for(self, website: Website) -> list:
        """
        Create message structure for Ollama chat.
        
        Args:
            website (Website): Website object to analyze
            
        Returns:
            list: Message structure for Ollama
        """
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt_for(website)}
        ]
    
    def summarize(self, url: str) -> str:
        """
        Scrape and summarize a website using local AI.
        
        Args:
            url (str): Website URL to analyze
            
        Returns:
            str: AI-generated summary in markdown format
        """
        try:
            # Scrape website
            website = Website(url)
            
            if website.status_code != 200:
                return f"❌ Failed to access website: {url}"
            
            # Generate summary using local AI
            messages = self.messages_for(website)
            
            logger.info(f"Generating summary for: {website.title}")
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            
            summary = response['message']['content']
            logger.info("Summary generated successfully")
            return summary
            
        except Exception as e:
            error_msg = f"Error generating summary: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def display_summary(self, url: str) -> None:
        """
        Generate and display a website summary in Jupyter notebook format.
        
        Args:
            url (str): Website URL to analyze and display
        """
        print(f"🔍 Analyzing: {url}")
        print("-" * 50)
        
        summary = self.summarize(url)
        
        try:
            # Display in Jupyter if available
            display(Markdown(summary))
        except:
            # Fallback to regular print
            print(summary)
    
    def batch_summarize(self, urls: list) -> Dict[str, str]:
        """
        Summarize multiple websites in batch.
        
        Args:
            urls (list): List of URLs to summarize
            
        Returns:
            dict: Dictionary mapping URLs to their summaries
        """
        results = {}
        
        for i, url in enumerate(urls, 1):
            print(f"Processing {i}/{len(urls)}: {url}")
            results[url] = self.summarize(url)
        
        return results


def main():
    """
    Example usage and testing function.
    
    This demonstrates the key capabilities of the LocalWebReader
    for business stakeholders and technical teams.
    """
    print("🤖 Local Web Reader - Cost-Effective AI Web Analysis")
    print("=" * 55)
    print(f"Model: {DEFAULT_MODEL}")
    print("Cost per request: $0 (after local setup)")
    print("Data privacy: 100% local processing")
    print()
    
    # Initialize reader
    reader = LocalWebReader()
    
    # Example analysis
    example_url = "https://www.cnn.com/2025/08/30/politics/zohran-mamdani-police-nypd-defund"
    
    print("📰 Example: News Article Analysis")
    reader.display_summary(example_url)


if __name__ == "__main__":
    main()

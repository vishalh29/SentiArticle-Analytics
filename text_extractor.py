import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging

def extract_article(url):
    """
    Extract article text from the given URL
    """
    try:
        # Send request
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['header', 'footer', 'nav', 'script', 'style']):
            element.decompose()
        
        # Extract title and article text
        title = soup.find('h1')
        article = soup.find('article') or soup.find(class_=['article', 'post-content', 'entry-content'])
        
        # Combine title and article text
        text_parts = []
        if title:
            text_parts.append(title.get_text().strip())
        if article:
            text_parts.append(article.get_text().strip())
        
        return '\n\n'.join(text_parts)
    
    except Exception as e:
        logging.error(f"Error extracting text from {url}: {str(e)}")
        return ""

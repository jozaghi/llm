import requests
import ollama
from bs4 import BeautifulSoup


def scrape_web_content(url: str) -> str:
    """Scrape the main content of a given URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.decompose()
    
    # Get text content
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    text = ' '.join(line for line in lines if line)
    
    return text


def generate_summary(content: str) -> str:
    """Generate a summary of the web content."""
    return ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": content}],
    )


def summarize_web_content(content: str) -> str:
    """Summarize the web content."""
    return generate_summary(content)


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Wikipedia:About"
    content = scrape_web_content(url)
    summary = summarize_web_content(content)
    print(summary['message']['content'])

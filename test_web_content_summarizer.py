import pytest
from unittest.mock import Mock, patch
from web_content_summerizer import scrape_web_content, generate_summary, summarize_web_content

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.text = """
        <html>
            <head>
                <script>var x = 1;</script>
                <style>.test{color:red;}</style>
            </head>
            <body>
                <h1>Test Title</h1>
                <p>Test content paragraph.</p>
            </body>
        </html>
    """
    return mock

@pytest.fixture
def mock_ollama_response():
    return {
        'message': {
            'content': 'Summarized content'
        }
    }

def test_scrape_web_content(mock_response):
    with patch('requests.get', return_value=mock_response):
        content = scrape_web_content('http://test.com')
        assert 'Test Title' in content
        assert 'Test content paragraph' in content
        assert 'var x = 1' not in content  # Script content should be removed
        assert '.test{color:red;}' not in content  # Style content should be removed

def test_generate_summary(mock_ollama_response):
    with patch('ollama.chat', return_value=mock_ollama_response):
        result = generate_summary('Test content')
        assert result == mock_ollama_response

def test_summarize_web_content(mock_ollama_response):
    with patch('ollama.chat', return_value=mock_ollama_response):
        result = summarize_web_content('Test content')
        assert result == mock_ollama_response 
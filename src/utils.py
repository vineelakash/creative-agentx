import re
import html

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing extra whitespace and stripping HTML tags.
    """
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Unescape HTML entities
    text = html.unescape(text)
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def safe_format(template: str, **kwargs) -> str:
    """
    Safely formats a string with keyword arguments, ignoring missing keys.
    """
    class SafeDict(dict):
        def __missing__(self, key):
            return '{' + key + '}'
    
    return template.format_map(SafeDict(**kwargs))

def count_tokens(text: str) -> int:
    """
    Returns an estimated token count for the given text.
    Uses a simple approximation: 1 token ~= 0.75 words.
    """
    if not text:
        return 0
    words = text.split()
    # Rough estimation: 1.3 tokens per word is a common heuristic for English
    return int(len(words) * 1.3)

def count_words(text: str) -> int:
    """
    Returns the word count of the text.
    """
    if not text:
        return 0
    return len(text.split())

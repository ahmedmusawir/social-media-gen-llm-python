import re
import requests
from io import BytesIO
from PIL import Image

# Function to download image from a URL and return it as bytes
def download_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    byte_arr = BytesIO()
    img.save(byte_arr, format="PNG")
    return byte_arr.getvalue()


def clean_text(text):
    """
    Function to clean text by removing leading/trailing spaces and replacing
    multiple spaces or newlines with a single space.
    
    Args:
        text (str): The text to be cleaned.
    
    Returns:
        str: The cleaned text.
    """
    # Remove leading and trailing spaces
    cleaned = text.strip()
    # Replace multiple spaces or newlines with a single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

def calculate_token_size(documents, model):
    """
    Function to calculate the total token size of a document.
    
    Args:
        documents (list): List of documents to calculate token size.
        model: The language model to use for token calculation.
    
    Returns:
        int: Total number of tokens in the document.
    """
    return sum(model.get_num_tokens(doc.page_content) for doc in documents)

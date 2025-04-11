import concurrent.futures
import requests
from bs4 import BeautifulSoup

# List of URLs to scrape
URLS = [
    "abcd",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
]

def fetch_title(url):
    """
    Fetch the title of a webpage given its URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        return url, title
    except requests.RequestException as e:
        return url, f"Error: {str(e)}"

def main():
    """
    Scrape web page titles in parallel using concurrent.futures.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks for parallel execution
        future_to_url = {executor.submit(fetch_title, url): url for url in URLS}
        
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                _, title = future.result()
                print(f"Title of {url}: {title}")
            except Exception as e:
                print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    main()

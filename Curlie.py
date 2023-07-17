import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def extract_urls(url, visited_urls, depth):
    if depth <= 0 or url in visited_urls:
        return
    
    # Add the URL to visited_urls to avoid duplicate processing
    visited_urls.add(url)
    
    try:
        # Send an HTTP request to fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all anchor tags and extract the href attribute (URLs)
        urls = soup.find_all('a')
        for link in urls:
            href = link.get('href')
            if href and href.startswith('http'):
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(url, href)
                print(absolute_url)
                
                # Recursively extract URLs from sub-pages
                extract_urls(absolute_url, visited_urls, depth - 1)
                
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching {url}: {str(e)}")

# Initial URL to start extraction
initial_url = "https://www.curlie.org"

# Set the maximum depth for recursion
max_depth = 3

# Set to store visited URLs
visited_urls = set()

# Start the recursive extraction
extract_urls(initial_url, visited_urls, max_depth)

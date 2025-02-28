import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse

# Base URL and domain restriction
BASE_URL = "https://segment.com/docs/"
DOMAIN = "segment.com"

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Track visited URLs to avoid duplicates
visited_urls = set()

# Recursive scraping function
def scrape_page(url, depth=0, max_depth=3):
    if depth > max_depth or url in visited_urls:
        return None
    
    print(f"Scraping: {url} (Depth: {depth})")
    visited_urls.add(url)
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Failed to retrieve {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract elements
    page_data = {
        "url": url,
        "title": soup.title.string if soup.title else "",
        "headings": {f"h{level}": [h.get_text(strip=True) for h in soup.find_all(f"h{level}")] for level in range(1, 7)},
        "paragraphs": [p.get_text(strip=True) for p in soup.find_all("p")],
        "lists": {
            "unordered": [[li.get_text(strip=True) for li in ul.find_all("li")] for ul in soup.find_all("ul")],
            "ordered": [[li.get_text(strip=True) for li in ol.find_all("li")] for ol in soup.find_all("ol")]
        },
        "code_blocks": [code.get_text(strip=True) for code in soup.find_all("code")],
        "blockquotes": [bq.get_text(strip=True) for bq in soup.find_all("blockquote")],
        "tables": [
            [[cell.get_text(strip=True) for cell in row.find_all(["th", "td"])] for row in table.find_all("tr")]
            for table in soup.find_all("table")
        ],
        "images": [urljoin(url, img["src"]) for img in soup.find_all("img", src=True)],
        "links": []
    }
    
    # Extract and follow internal links
    for a in soup.find_all("a", href=True):
        link = urljoin(url, a["href"])
        parsed_link = urlparse(link)
        
        if parsed_link.netloc.endswith(DOMAIN) and link.startswith(BASE_URL) and link not in visited_urls:
            page_data["links"].append(link)
            time.sleep(1)  # Avoid overloading the server
            sub_page_data = scrape_page(link, depth=depth+1, max_depth=max_depth)
            if sub_page_data:
                scraped_data.append(sub_page_data)
    
    return page_data

# Start scraping
scraped_data = []
scraped_data.append(scrape_page(BASE_URL))

# Save data to JSON
with open("segment_scraped_data.json", "w", encoding="utf-8") as json_file:
    json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

print("✅ Data scraped successfully! Saved to segment_scraped_data.json")


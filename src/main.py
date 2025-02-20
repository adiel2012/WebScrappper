from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import time
import re
import logging
from typing import Set, List

class WebScraper:
    def __init__(self, base_url: str, output_folder: str = "scraped_pages", max_pages: int = 50, wait_time: int = 5):
        self.base_url = base_url
        self.output_folder = output_folder
        self.max_pages = max_pages
        self.wait_time = wait_time
        self.visited_urls: Set[str] = set()
        self.urls_to_visit: List[str] = [base_url]
        
        # Create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # Setup logging
        logging.getLogger('selenium').setLevel(logging.CRITICAL)
        
        # Initialize driver
        self.driver = self.setup_driver()
        self.wait = WebDriverWait(self.driver, wait_time)

    def setup_driver(self):
        """Configure and initialize Chrome in headless mode."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        return webdriver.Chrome(options=chrome_options)

    def get_safe_filename(self, url: str) -> str:
        """Convert URL to a safe filename."""
        path = urlparse(url).path.strip('/')
        if not path:
            path = 'index'
        
        safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', path)
        safe_name = safe_name[:150] if len(safe_name) > 150 else safe_name
        
        # Add a number if file exists
        base_name = safe_name
        counter = 1
        while os.path.exists(os.path.join(self.output_folder, f"{safe_name}.txt")):
            safe_name = f"{base_name}_{counter}"
            counter += 1
        
        return f"{safe_name}.txt"

    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the same domain and is not a file."""
        try:
            parsed_url = urlparse(url)
            base_domain = urlparse(self.base_url).netloc
            
            # Check if same domain and not a file
            return (parsed_url.netloc == base_domain and
                   not any(url.lower().endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.gif']))
        except:
            return False

    def extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extract valid links from the page."""
        links = []
        for link in soup.find_all('a', href=True):
            url = urljoin(current_url, link['href'])
            if self.is_valid_url(url):
                links.append(url)
        return links

    def save_content(self, url: str, content: str) -> str:
        """Save content to a file and return the filepath."""
        filename = self.get_safe_filename(url)
        filepath = os.path.join(self.output_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Source URL: {url}\n")
            f.write(f"Scraped on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 80 + "\n\n")
            f.write(content)
        
        return filepath

    def scrape_page(self, url: str) -> List[str]:
        """Scrape a single page and return found links."""
        try:
            print(f"\n📄 Scraping: {url}")
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(self.wait_time)
            
            # Parse page
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style']):
                element.decompose()
            
            # Extract text
            content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                                           'div', 'span', 'article', 'section', 'main'])
            
            text_content = []
            for element in content_elements:
                text = element.get_text().strip()
                if text:
                    text_content.append(text)
            
            # Save content
            if text_content:
                content = '\n\n'.join(text_content)
                filepath = self.save_content(url, content)
                
                print(f"✅ Saved to: {filepath}")
                print(f"📊 Size: {os.path.getsize(filepath) / 1024:.1f} KB")
                print(f"📝 Blocks: {len(text_content)}")
            
            # Return new links
            return self.extract_links(soup, url)
            
        except Exception as e:
            print(f"❌ Error scraping {url}: {str(e)}")
            return []

    def scrape_site(self):
        """Scrape the entire site up to max_pages."""
        try:
            print(f"\n🌐 Starting to scrape: {self.base_url}")
            print(f"📁 Saving to folder: {self.output_folder}")
            print(f"🔄 Maximum pages: {self.max_pages}")
            print("=" * 50)
            
            while self.urls_to_visit and len(self.visited_urls) < self.max_pages:
                # Get next URL
                current_url = self.urls_to_visit.pop(0)
                if current_url in self.visited_urls:
                    continue
                
                # Scrape page and get new links
                new_links = self.scrape_page(current_url)
                self.visited_urls.add(current_url)
                
                # Add new links to visit
                for link in new_links:
                    if (link not in self.visited_urls and 
                        link not in self.urls_to_visit):
                        self.urls_to_visit.append(link)
                
                print(f"\n📊 Progress: {len(self.visited_urls)}/{self.max_pages} pages")
                print(f"🔍 URLs in queue: {len(self.urls_to_visit)}")
            
            print("\n✨ Scraping completed!")
            print(f"📚 Total pages scraped: {len(self.visited_urls)}")
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Scraping interrupted by user")
        finally:
            self.driver.quit()

def main():
    print("\n🌐 Web Page Content Scraper")
    print("=" * 30)
    
    # Get input from user
    url = input("\nEnter the website URL to scrape: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    output_folder = input("Enter output folder name (press Enter for default 'scraped_pages'): ").strip()
    output_folder = output_folder or "scraped_pages"
    
    max_pages = input("Enter maximum number of pages to scrape (press Enter for default 50): ").strip()
    try:
        max_pages = int(max_pages) if max_pages else 50
    except ValueError:
        max_pages = 50
    
    wait_time = input("Enter page load wait time in seconds (press Enter for default 5): ").strip()
    try:
        wait_time = int(wait_time) if wait_time else 5
    except ValueError:
        wait_time = 5
    
    # Create and run scraper
    scraper = WebScraper(
        base_url=url,
        output_folder=output_folder,
        max_pages=max_pages,
        wait_time=wait_time
    )
    
    scraper.scrape_site()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
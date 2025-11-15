#!/usr/bin/env python3
"""
Berkshire Hathaway Website Extractor
Extracts and organizes all materials from berkshirehathaway.com
"""

import os
import re
import time
import hashlib
from urllib.parse import urljoin, urlparse, urlunparse
from pathlib import Path
from collections import deque
import mimetypes

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required packages not installed. Please run: pip install requests beautifulsoup4")
    exit(1)


class BerkshireExtractor:
    def __init__(self, base_url="https://www.berkshirehathaway.com/", output_dir="berkshire_materials"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.visited_urls = set()
        self.downloaded_files = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Category directories
        self.categories = {
            'html_pages': self.output_dir / 'html_pages',
            'pdf_documents': self.output_dir / 'pdf_documents',
            'images': self.output_dir / 'images',
            'stylesheets': self.output_dir / 'stylesheets',
            'scripts': self.output_dir / 'scripts',
            'text_files': self.output_dir / 'text_files',
            'other': self.output_dir / 'other'
        }

        # Create directories
        for category_dir in self.categories.values():
            category_dir.mkdir(parents=True, exist_ok=True)

    def is_valid_url(self, url):
        """Check if URL belongs to the target domain"""
        parsed = urlparse(url)
        base_parsed = urlparse(self.base_url)
        return parsed.netloc == base_parsed.netloc or parsed.netloc == ''

    def normalize_url(self, url):
        """Normalize URL to avoid duplicates"""
        parsed = urlparse(url)
        # Remove fragment
        normalized = urlunparse(parsed._replace(fragment=''))
        return normalized

    def categorize_url(self, url, content_type=None):
        """Determine category based on URL and content type"""
        url_lower = url.lower()

        if content_type:
            if 'pdf' in content_type:
                return 'pdf_documents'
            elif 'image' in content_type:
                return 'images'
            elif 'css' in content_type or 'stylesheet' in content_type:
                return 'stylesheets'
            elif 'javascript' in content_type or 'script' in content_type:
                return 'scripts'
            elif 'html' in content_type:
                return 'html_pages'
            elif 'text' in content_type:
                return 'text_files'

        # Fallback to extension-based categorization
        if url_lower.endswith('.pdf'):
            return 'pdf_documents'
        elif url_lower.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp')):
            return 'images'
        elif url_lower.endswith('.css'):
            return 'stylesheets'
        elif url_lower.endswith(('.js', '.json')):
            return 'scripts'
        elif url_lower.endswith(('.html', '.htm')):
            return 'html_pages'
        elif url_lower.endswith(('.txt', '.csv')):
            return 'text_files'
        else:
            return 'other'

    def get_safe_filename(self, url, content_type=None):
        """Generate a safe filename from URL"""
        parsed = urlparse(url)
        path = parsed.path

        if not path or path == '/':
            filename = 'index.html'
        else:
            filename = os.path.basename(path)
            if not filename:
                filename = 'page.html'

        # If no extension, try to add one based on content type
        if '.' not in filename:
            ext = mimetypes.guess_extension(content_type) if content_type else None
            if ext:
                filename += ext
            else:
                filename += '.html'

        # Sanitize filename
        filename = re.sub(r'[^\w\-_\. ]', '_', filename)

        # Add hash to avoid collisions
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{url_hash}{ext}"

        return filename

    def download_file(self, url):
        """Download a file and save it to appropriate category"""
        url = self.normalize_url(url)

        if url in self.downloaded_files:
            return

        try:
            print(f"Downloading: {url}")
            response = self.session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()

            content_type = response.headers.get('content-type', '').lower()
            category = self.categorize_url(url, content_type)
            filename = self.get_safe_filename(url, content_type)
            filepath = self.categories[category] / filename

            # Save file
            with open(filepath, 'wb') as f:
                f.write(response.content)

            self.downloaded_files.add(url)
            print(f"  ✓ Saved to: {category}/{filename}")

            # If it's HTML, extract links
            if category == 'html_pages' or 'html' in content_type:
                return response.content

        except Exception as e:
            print(f"  ✗ Error downloading {url}: {e}")

        return None

    def extract_links(self, html_content, base_url):
        """Extract all links from HTML content"""
        links = set()

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract all href links
            for tag in soup.find_all(['a', 'link']):
                href = tag.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    if self.is_valid_url(full_url):
                        links.add(full_url)

            # Extract all src links (images, scripts, etc.)
            for tag in soup.find_all(['img', 'script', 'iframe', 'embed', 'source']):
                src = tag.get('src')
                if src:
                    full_url = urljoin(base_url, src)
                    if self.is_valid_url(full_url):
                        links.add(full_url)

            # Extract CSS urls
            for tag in soup.find_all('style'):
                if tag.string:
                    css_urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', tag.string)
                    for css_url in css_urls:
                        full_url = urljoin(base_url, css_url)
                        if self.is_valid_url(full_url):
                            links.add(full_url)

        except Exception as e:
            print(f"  Error extracting links: {e}")

        return links

    def crawl(self, max_pages=None):
        """Crawl the website and download all materials"""
        queue = deque([self.base_url])
        pages_crawled = 0

        print(f"\n{'='*60}")
        print(f"Starting extraction from: {self.base_url}")
        print(f"Output directory: {self.output_dir}")
        print(f"{'='*60}\n")

        while queue:
            if max_pages and pages_crawled >= max_pages:
                break

            url = queue.popleft()
            url = self.normalize_url(url)

            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)
            pages_crawled += 1

            print(f"\n[Page {pages_crawled}] Crawling: {url}")

            # Download the file
            html_content = self.download_file(url)

            # If it's HTML, extract and queue links
            if html_content:
                links = self.extract_links(html_content, url)
                for link in links:
                    normalized_link = self.normalize_url(link)
                    if normalized_link not in self.visited_urls:
                        queue.append(link)

                print(f"  Found {len(links)} new links")

            # Be respectful - add small delay
            time.sleep(0.5)

        self.print_summary()

    def print_summary(self):
        """Print extraction summary"""
        print(f"\n{'='*60}")
        print(f"EXTRACTION COMPLETE")
        print(f"{'='*60}")
        print(f"Total URLs visited: {len(self.visited_urls)}")
        print(f"Total files downloaded: {len(self.downloaded_files)}")
        print(f"\nFiles by category:")

        for category_name, category_path in self.categories.items():
            file_count = len(list(category_path.glob('*')))
            if file_count > 0:
                print(f"  {category_name}: {file_count} files")

        print(f"\nAll materials saved to: {self.output_dir.absolute()}")
        print(f"{'='*60}\n")


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     Berkshire Hathaway Website Extractor                ║
    ║     Extracts all materials from berkshirehathaway.com    ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Initialize extractor
    extractor = BerkshireExtractor()

    # Start crawling (set max_pages=None to crawl entire site)
    # For testing, you might want to start with a smaller number
    extractor.crawl(max_pages=None)


if __name__ == "__main__":
    main()

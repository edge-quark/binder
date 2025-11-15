# Berkshire Hathaway Website Extractor

A comprehensive web scraper that extracts and organizes all materials from the Berkshire Hathaway website (https://www.berkshirehathaway.com/).

## Features

- **Comprehensive Crawling**: Automatically discovers and downloads all linked content from the website
- **Smart Categorization**: Organizes downloaded materials into categories:
  - `html_pages/` - HTML web pages
  - `pdf_documents/` - PDF files (annual reports, letters, etc.)
  - `images/` - All image files (JPG, PNG, GIF, SVG, etc.)
  - `stylesheets/` - CSS files
  - `scripts/` - JavaScript files
  - `text_files/` - Text and CSV files
  - `other/` - Any other file types
- **Duplicate Prevention**: Tracks visited URLs and downloaded files to avoid duplicates
- **Progress Tracking**: Shows real-time progress of the extraction process
- **Respectful Crawling**: Includes delays between requests to be respectful to the server

## Installation

### Prerequisites

- Python 3.6 or higher

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4
```

## Usage

### Option 1: Run on GitHub (Recommended)

You can run the extractor directly on GitHub using GitHub Actions - no local setup required!

1. Go to your repository on GitHub
2. Click on the **Actions** tab
3. Select **Run Berkshire Hathaway Extractor** from the workflows list
4. Click **Run workflow** button
5. Configure options:
   - **max_pages**: Leave empty for full extraction, or enter a number (e.g., `50`) for testing
   - **output_dir**: Leave as default or customize
6. Click the green **Run workflow** button
7. Wait for the workflow to complete (check progress in the Actions tab)
8. Download the extracted materials as a ZIP artifact from the workflow run

The extracted materials will be packaged as `berkshire-materials.tar.gz` and available for download for 7 days.

### Option 2: Run Locally

Run the extractor with default settings on your local machine:

```bash
python berkshire_extractor.py
```

This will:
1. Start crawling from https://www.berkshirehathaway.com/
2. Download all discovered materials
3. Save everything to `berkshire_materials/` directory in categorized folders

### Advanced Usage

You can customize the extractor by modifying the code:

```python
from berkshire_extractor import BerkshireExtractor

# Create extractor with custom output directory
extractor = BerkshireExtractor(
    base_url="https://www.berkshirehathaway.com/",
    output_dir="my_custom_folder"
)

# Limit to first 50 pages (useful for testing)
extractor.crawl(max_pages=50)

# Or crawl entire site
extractor.crawl(max_pages=None)
```

## Output Structure

After running, you'll have a directory structure like this:

```
berkshire_materials/
├── html_pages/
│   ├── index_a1b2c3d4.html
│   ├── letters_e5f6g7h8.html
│   └── ...
├── pdf_documents/
│   ├── 2023_annual_report_i9j0k1l2.pdf
│   ├── chairman_letter_m3n4o5p6.pdf
│   └── ...
├── images/
│   ├── logo_q7r8s9t0.png
│   └── ...
├── stylesheets/
│   └── style_u1v2w3x4.css
├── scripts/
│   └── script_y5z6a7b8.js
├── text_files/
│   └── ...
└── other/
    └── ...
```

Note: Files are renamed with a hash suffix to prevent naming conflicts.

## Features Explained

### URL Normalization

The extractor normalizes URLs to prevent downloading the same content multiple times (e.g., `page.html` and `page.html#section` are treated as the same page).

### Smart Categorization

Files are categorized using:
1. HTTP Content-Type headers (primary method)
2. File extension fallback (secondary method)

### Link Discovery

The extractor finds links from:
- Anchor tags (`<a href="...">`)
- Link tags (`<link href="...">`)
- Images (`<img src="...">`)
- Scripts (`<script src="...">`)
- Stylesheets (`<link rel="stylesheet">`)
- CSS url() references
- iframes, embeds, and other media

### Safety Features

- Only downloads from the berkshirehathaway.com domain
- Respects server resources with delays between requests
- Handles errors gracefully and continues crawling
- Generates safe filenames from URLs

## Troubleshooting

### SSL/TLS Errors

If you encounter SSL errors, you may need to update your system's SSL certificates or use:

```python
import requests
requests.packages.urllib3.disable_warnings()
```

### Memory Issues

For very large sites, you might want to process in batches:

```python
extractor.crawl(max_pages=100)  # Process 100 pages at a time
```

### Connection Timeouts

The default timeout is 30 seconds. You can modify this in the code:

```python
response = self.session.get(url, timeout=60)  # 60 second timeout
```

## Legal and Ethical Considerations

- This tool is for personal research and archival purposes
- Respect the website's robots.txt file
- Be mindful of server load
- Ensure compliance with the website's terms of service
- The tool includes delays to be respectful to the server

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues or pull requests for improvements.

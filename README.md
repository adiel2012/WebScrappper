# Web Content Scraper

A Python-based web scraper that extracts content from websites and saves each page as a separate text file. This tool is particularly useful for creating training datasets for Large Language Models (LLMs) or for archiving web content.

## Features

- 🌐 Scrapes multiple pages from a website automatically
- 📁 Saves each page as a separate text file
- 🔍 Follows internal links within the same domain
- ⚙️ Configurable scraping parameters
- 🚀 Handles dynamic JavaScript-rendered content
- 📊 Progress tracking and statistics

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/web-content-scraper.git
cd web-content-scraper
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Unix/macOS
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python src/main.py
```

2. Follow the prompts:
   - Enter the website URL to scrape
   - Specify output folder name (optional)
   - Set maximum number of pages to scrape (optional)
   - Set page load wait time (optional)

Example:
```
🌐 Web Page Content Scraper
==============================

Enter the website URL to scrape: help.com
Enter output folder name (press Enter for default 'scraped_pages'): docs
Enter maximum number of pages to scrape (press Enter for default 50): 20
Enter page load wait time in seconds (press Enter for default 5):
```

## Output

The scraper creates a folder structure like this:
```
output_folder/
├── index.txt
├── about.txt
├── products.txt
└── ...
```

Each text file contains:
- Source URL
- Scraping timestamp
- Page content with proper formatting

## Configuration

Default settings:
- Max pages: 50
- Wait time: 5 seconds
- Output folder: 'scraped_pages'

## Features in Detail

### Content Extraction
- Extracts text from various HTML elements
- Removes unwanted elements (scripts, styles)
- Preserves text formatting
- Handles dynamic content

### URL Management
- Follows internal links only
- Avoids duplicate pages
- Handles relative and absolute URLs
- Excludes non-HTML resources (PDFs, images)

### File Management
- Creates unique filenames
- Handles filename collisions
- UTF-8 encoding support
- Organized folder structure

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Your Name - Initial work

## Acknowledgments

- Selenium WebDriver for browser automation
- BeautifulSoup4 for HTML parsing
- Chrome DevTools for web debugging
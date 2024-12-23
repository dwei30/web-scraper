# Web Scraper

This is a Python-based web scraper that extracts data from a given URL and writes this data to a CSV file. The scraper uses `Selenium` for navigating and interacting with the web page and `BeautifulSoup` for parsing the page's HTML content. This code is designed speciafically to retrieve multiple job listings from a given URL.

## Features

- **URL Validation**: Ensures the input URL is valid before starting the scraping.
- **Page Load Wait**: Waits for the page to load fully before extracting data.
- **Error Handling**: Retries pages that fail to load within the specified timeout.
- **CSV Output**: Outputs the scraped data to a CSV file for easy data handling.
- **Pagination**: Supports navigating through multiple pages if the site contains more job listings.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.x
- [Selenium](https://pypi.org/project/selenium/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (Make sure the ChromeDriver version matches your installed Chrome browser version)

You can install the required Python libraries using `pip`:

```bash
pip install selenium beautifulsoup4
```


# DISCLAIMER

This project is a work in progress, and bugs may exist. While the script performs its intended function to extract job listings, it may encounter issues on certain websites or with specific types of data. Please use this tool with caution, and feel free to report any issues or suggestions for improvement.
# Web Scraper

This is a Python-based web scraper script that extracts data from a given URL and writes this data to a CSV file. The scraper uses `Selenium` for navigating and interacting with the web page and `BeautifulSoup` for parsing the page's HTML content. This code is designed speciafically to retrieve multiple job listings from a given URL.

> **Note**: This script is specifically designed to work with [https://www.babymap.hk/](https://www.babymap.hk/explore/). If you wish to use this scraper on a different website, you will likely need to modify the script to account for differences in the website's structure and HTML elements.

## Requirements

Before running the script, ensure you have the following installed:

- Python 3.x
- [Selenium](https://pypi.org/project/selenium/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [ChromeDriver](https://developer.chrome.com/docs/chromedriver) (Make sure the ChromeDriver version matches your installed Chrome browser version)

You can install the required Python libraries using `pip`:

```bash
pip install selenium beautifulsoup4
```

## Setup
1. Clone or download this repository.
2. Ensure that `chromedriver` is installed and accessible from your PATH.
3. Install the required dependencies with `pip`.

## Usage

1. Run the Script:
Open your terminal and run the script by executing the following command:
```bash
python main.py
```
2. Enter the URL: When prompted, input the URL of the listing page you wish to scrape.
3. Data Extraction: The script will begin scraping the page listings from the provided URL. For the code specifically, it will collect:
    - Page Name
    - Location
    - Phone Number
    - Page URL
4. CSV Output: The extracted data will be written to a file named postings.csv. If the file already exists, the data will be appended to it.
5. If the site has multiple pages, the script will automatically navigate to the next page and continue scraping until there are no more pages.

# Disclaimer

This project is a work in progress, and as such, bugs may exist. While the script performs its intended function, it may encounter issues on certain websites or with specific types of data. Please use this tool with caution.

**Do not abuse this scraper.** Always respect the website's Terms of Service. Excessive scraping or failure to comply with a website's usage policies may result in your IP being blocked or other legal consequences. Be mindful of server load by limiting request frequency.

This script is provided "as is". The author assumes no responsibility for any issues, damages, or legal consequences arising from its use. By using this tool, you agree to do so at your own risk and in compliance with applicable laws and website policies.


import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException


# URL validation function
def isValidUrl(url):
    return url.startswith('http://') or url.startswith('https://')

# Get URL from user and validate
while True:
    inputURL = input("Please enter a valid URL: ")
    
    if not isValidUrl(inputURL):
        print("Invalid URL. Please try again. (Must include http:// or https://)")
        continue

    # Initialize the web driver (Make sure to have ChromeDriver installed)
    # If using a different browser, replace 'webdriver.Chrome()' with the relevant driver
    # and ensure the driver is compatible with the browser version.driver = webdriver.Chrome()
    try:
        driver = webdriver.Chrome()
        driver.get(inputURL)
        break
    except WebDriverException as e:
        print("Error loading website. Please try again.")
        driver.quit()

# Display graphic and disclaimer
print('''
 __          __  _     _____                                
 \ \        / / | |   / ____|                               
  \ \  /\  / /__| |__| (___   ___ _ __ __ _ _ __   ___ _ __ 
   \ \/  \/ / _ \ '_  \___ \ / __| '__/ _` | '_ \ / _ \ '__|
    \  /\  /  __/ |_) |___) | (__| | | (_| | |_) |  __/ |   
     \/  \/ \___|_.__/_____/ \___|_|  \__,_| .__/ \___|_|   
                                           | |              
                                           |_|              
''')

print('This is experimental, things may break. Please use with caution, DO NOT ABUSE!\n')

# Check if the website loads
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    while True:
        startScraping = input("The website has loaded. Would you like to start? (y/n): ").strip().lower()
        if startScraping == 'y':
            break
        elif startScraping == 'n':
            print("Exiting program. Bye Bye.")
            driver.quit()
            exit()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
except Exception as e:
    print("Error loading website. Exiting program.")
    driver.quit()
    exit()

# CSV setup (Change the CSV filename or headers if needed for different data types)
csvFile = 'postings.csv'
csv_headers = ['Name', 'Location', 'Phone Number', 'URL']

# Check if CSV file exists, otherwise create it
try:
    with open(csvFile, 'r', encoding='utf-8'):
        print("\nExisting CSV file found.")
except FileNotFoundError:
    print('\nCSV file not found. Creating new file...')
    with open(csvFile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

# Wait for page to load
def waitForPageLoad(driver, timeout=10, maxWaitTime = 20):
    startTime = time.time()
    while True:
        try:
            # Adjust the CSS selector below based on the website's page structure
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.grid-item'))
            )
            return True
        except Exception as e:
            if time.time() - startTime > maxWaitTime:
                print(f"Timeout reached ({maxWaitTime} seconds), retrying...")
                return False
            time.sleep(1)

# Main scraping loop
while True:
    print("\nExtracting Data...")

    # Wait for page to load
    if not waitForPageLoad(driver, timeout=10, maxWaitTime=20):
        print("Page did not load properly within time limit, retrying...")
        driver.refresh()
        time.sleep(5)
        continue

    # Grab HTML and parse (Change selectors based on the website's HTML structure)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'lxml')

   # Adjust the selector below to match the container holding the data on the target website
    centrePostings = soup.find_all('div', class_='col-md-12 grid-item')

    # Loop through all job postings (Modify based on data requirements and HTML layout)
    for post in centrePostings:
        try:

            # Extract name (Update tag and class to match the website)
            postName = post.find('h4', class_='case27-primary-text listing-preview-title').text.strip()
            
            # Extract location (Modify if website has different structure for categories)
            postCategories = post.find_all('span', class_='category-name')
            location = postCategories[1].text if len(postCategories) > 1 else "Unknown"

            # Extract URL (Ensure the link structure matches the site, add base URL if necessary)
            post_url = post.find('a')['href']
            if not post_url.startswith("http"):
                post_url = 'https://www.babymap.hk' + post_url  # Change base URL to match target website

            # Navigate to the individual posting page
            driver.get(post_url)
            time.sleep(1)  # Adjust wait time if page loading is slow

            # Extract phone number (Update CSS selector if the phone link structure differs)
            postPageHTML = driver.page_source
            postSoup = BeautifulSoup(postPageHTML, 'lxml')
            phoneLink = postSoup.select_one("a[href^='tel:']")
            phoneNumber = phoneLink['href'].replace('tel:', '').replace('%20', ' ') if phoneLink else "No phone number found"

            # Write data to CSV (Ensure headers match the data being scraped)
            with open(csvFile, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([postName, location, phoneNumber, post_url])
                print(f'{postName}, {location}, {phoneNumber}, {post_url}')
        except Exception as e:
            print(f"Error processing posting: {e}")
            continue

    # Find the 'next' button and navigate to the next page (Customize selector for pagination buttons)
    nextButton = soup.find('a', rel='next') # Adjust based on website structure
    if not nextButton:
        print("\nNo more pages found.")
        break
    else:
        print("\nAdditional pages found.")

    # Get the next page URL and navigate
    nextPageUrl = nextButton['href']    # Ensure the href attribute structure matches the site
    driver.get(nextPageUrl)
    driver.get(nextPageUrl)
    time.sleep(5)   # Adjust wait time if next page loading is slow

print('\nData has been written to CSV file.')
print('Bye Bye.\n')
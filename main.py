import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL validation function
def isValidUrl(url):
    return url.startswith('http://') or url.startswith('https://')

# Load webpage to get results

# Get URL from user and validate
while True:
    inputURL = input("Please enter a valid URL: ")
    if not isValidUrl(inputURL):
        print("Invalid URL. Please try again.")
    else:
        break

# Initialize the web driver
driver = webdriver.Chrome()
driver.get(inputURL)

# CSV setup
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

# Display graphic and disclaimer

print('''
 __          __  _     _____                                
 \ \        / / | |   / ____|                               
  \ \  /\  / /__| |__| (___   ___ _ __ __ _ _ __   ___ _ __ 
   \ \/  \/ / _ \ '_  \\___ \ / __| '__/ _` | '_ \ / _ \ '__|
    \  /\  /  __/ |_) |___) | (__| | | (_| | |_) |  __/ |   
     \/  \/ \___|_.__/_____/ \___|_|  \__,_| .__/ \___|_|   
                                           | |              
                                           |_|              
''')

print('This is experimental, things may break. Please use with caution!')

# Wait for page to load
def waitForPageLoad(driver, timeout=10, maxWaitTime = 20):
    startTime = time.time()
    while True:
        try:
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

    # Grab HTML and parse
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'lxml')
    centrePostings = soup.find_all('div', class_='col-md-12 grid-item')

    # Loop through all job postings
    for post in centrePostings:
        try:

            postName = post.find('h4', class_='case27-primary-text listing-preview-title').text.strip()
            postCategories = post.find_all('span', class_='category-name')

            location = postCategories[1].text if len(postCategories) > 1 else "Unknown"

            post_url = post.find('a')['href']
            if not post_url.startswith("http"):
                post_url = 'https://www.babymap.hk' + post_url

            driver.get(post_url)
            time.sleep(1)  # Wait for page to load

            # Extract phone number from individual posting
            postPageHTML = driver.page_source
            postSoup = BeautifulSoup(postPageHTML, 'lxml')
            phoneLink = postSoup.select_one("a[href^='tel:']")
            phoneNumber = phoneLink['href'].replace('tel:', '').replace('%20', ' ') if phoneLink else "No phone number found"

            # Write data to CSV
            with open(csvFile, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([postName, location, phoneNumber, post_url])
                print(f'{postName}, {location}, {phoneNumber}, {post_url}')
        except Exception as e:
            print(f"Error processing posting: {e}")
            continue

    # Find the 'next' button and navigate to the next page
    nextButton = soup.find('a', rel='next')
    if not nextButton:
        print("\nNo more pages found.")
        break
    else:
        print("\nAdditional pages found.")

    # Get the next page URL and navigate
    nextPageUrl = nextButton['href']

    driver.get(nextPageUrl)
    time.sleep(5)

print('\nData has been written to CSV file.')
print('Bye Bye.\n')

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# Load webpage to get results

print('\nThis is experimental, please use with caution!\n')
inputURL = input("Please enter URL: ")

driver = webdriver.Chrome()
driver.get(inputURL)

all_postings = []

# Set up CSV file to save data written
csvFile = 'postings.csv'
csv_headers = ['Name', 'Location', 'Phone Number']

try:
    with open(csvFile, 'r', encoding='utf-8'):
        print("\nExisitng CSV file exists")
        pass  # If the file exists, no need to do anything
except FileNotFoundError:
    print('\nCSV file not found. Creating new file...')
    with open(csvFile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

def waitForPageLoad(driver, timeout=10):
    try:
        # Wait for at least one posting (div with class 'grid-item') to load
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.grid-item')))
        return True
    except Exception as e:
        print("Error waiting for page load:", e)
        return False

while True:

    print("\nExtracting Data...")

    # Ensure the main page has loaded
    if not waitForPageLoad(driver):
        print("Page did not load properly, retrying...")
        driver.refresh()
        time.sleep(5)
        continue

    # Grab HTML text from the current page
    html_text = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(html_text, 'lxml')
    centrePostings = soup.find_all('div', class_='col-md-12 grid-item')

    for post in centrePostings:
        try:
            postName = post.find('h4', class_='case27-primary-text listing-preview-title').text.strip()
            postCategories = post.find_all('span', class_='category-name')

            #print(postName)

            if len(postCategories) > 1:
                location = postCategories[1].text
                #print(location)

            # Get the URL of the individual posting
            post_url = post.find('a')['href']
            
            # Ensure post_url is a complete URL
            if not post_url.startswith("http"):
                post_url = 'https://www.babymap.hk' + post_url
            
            driver.get(post_url)

            # No need to wait for the individual page to load completely
            time.sleep(1)  # Just a short wait

            # Extract the phone number if available
            postPageHTML = driver.page_source
            postSoup = BeautifulSoup(postPageHTML, 'lxml')

            phoneLink = postSoup.select_one("a[href^='tel:']")
            if phoneLink:
                phoneNumber = phoneLink['href'].replace('tel:', '').replace('%20', ' ')
                #print(phoneNumber)
            else:
                print("No Phone number found")

            with open(csvFile, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([postName, location, phoneNumber]) 
                print(f'{postName}, {location}, {phoneNumber}')

        except Exception as e:
            print(f'Error processing posting: {e}')
            continue

    # Find the 'next' button and navigate to the next page
    nextButton = soup.find('a', rel='next')
    
    if not nextButton:
        print("No more pages found")
        break
    else:
        print("Additional pages found")

    # Navigate to the next page
    nextPageUrl = nextButton['href']
    
    # Ensure nextPageUrl is a complete URL
    if not nextPageUrl.startswith("http"):
        nextPageUrl = 'https://www.babymap.hk' + nextPageUrl
    
    driver.get(nextPageUrl)
    time.sleep(5)
    break

print('Data has been written to CSV file.')
print('Bye Bye')
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

# load webpage to get results
driver = webdriver.Chrome()
driver.get('https://www.babymap.hk/explore')


all_postings = []

while True:

    # grab html text from webpage
    html_text = driver.page_source

    time.sleep(5)

    # find all postings
    soup = BeautifulSoup(html_text, 'lxml')
    centrePostings = soup.find_all('div', class_ = 'col-md-12 grid-item')

    for post in centrePostings:
        postName = post.find('h4', class_ = 'case27-primary-text listing-preview-title').text.replace('                ','')
        postCatagories = post.find_all('span', class_ = 'category-name')

        print(postName)
        print(postCatagories[1].text)

        NameE
        

    # find next page element
    nextButton = soup.find('a', rel = 'next')

    if not nextButton:
        break

    driver.get(nextButton['href'])

    time.sleep(5)
    break

    

# print(centrePostings[0])

with open('page_content.txt', 'w', encoding='utf-8') as f:
    for text in centrePostings:
        f.write(str(text))

# with open('home.html')
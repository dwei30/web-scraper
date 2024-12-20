from bs4 import BeautifulSoup

import requests

html_text = requests.get('https://www.babymap.hk/explore/?sort=random').text
# print(html_text)

with open('page_content.txt', 'w', encoding='utf-8') as f:
    f.write(html_text)

soup = BeautifulSoup(html_text, 'lxml')
centrePostings = soup.find_all('div', class_ = 'col-md-12 grid-item')

print(centrePostings)

# with open('home.html')
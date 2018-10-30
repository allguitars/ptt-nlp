import ptt
import requests
import json
from bs4 import BeautifulSoup

soup, session = ptt.get_first_soup('Tech_Job')

# The first article
index = 1
print(f'---------------------- {index} ----------------------')
a = soup.find(class_='r-ent')
print(a.select('.title > a')[0].string)
print(a.select('.author')[0].string)

# 印出所有文章標題  除了置底文
index += 1
while('r-list-sep' not in a.next_sibling.next_sibling.get('class')):
    print(f'---------------------- {index} ----------------------')
    a = a.next_sibling.next_sibling
    # Title and Link
    if a.select('.title > a'):
        print('標題:', a.select('.title > a')[0].string)
    else:
        print(a.select('.title')[0].string.strip())
    # Author
    print('作者:', a.select('.author')[0].string)
    # Highlight
    if a.find(class_='hl'):
        print('推文:', a.select('.hl')[0].string)
    else:
        print('推文:', '尚無推文')

    index += 1

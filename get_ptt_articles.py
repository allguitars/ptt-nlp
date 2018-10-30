import ptt
import requests
import json
from bs4 import BeautifulSoup

soup, session = ptt.get_first_soup('Tech_Job')
articles = ptt.parse_info(soup)

# Check the content
ptt.show_json_list(articles)

# Get previous page ==========================================================
# prev_plink = ptt.get_prev_plink(soup)
#
# soup = ptt.get_soup(session, prev_plink)
# ptt.show_all(soup)

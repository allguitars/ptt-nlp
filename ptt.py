import requests
import json
from bs4 import BeautifulSoup

PTT_ROOT = 'https://www.ptt.cc'
restricted = ['Gossiping']


def get_first_soup(board):
    """
    Get the first page of PTT. It will return both the soup and session
    because this is the firts time to visit the restricted boards.

    :return: <BeautifulSoup>, <Session>
    """
    payload_url = '/bbs/' + board + '/index.html'  # /bbs/Gossiping/index.html
    url = PTT_ROOT + payload_url  # https://www.ptt.cc/bbs/Gossiping/index.html
    session = requests.Session()

    if board in restricted:
        payload = {'from': payload_url, 'yes': 'yes'}
        # Get the session because you have to click "YES" on the welcome page
        # This session instance holds the cookie. So use it to get/post later.
        session.post('https://www.ptt.cc/ask/over18', data=payload)
        res = session.get(url)
        # print(type(res))  # <class 'requests.models.Response'>
        soup = BeautifulSoup(res.text, 'html.parser')
        # print(type(soup))  # <class 'bs4.BeautifulSoup'>

        return soup, session
    else:
        res = session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        return soup, session


def get_soup(session, link):
    """
    :param session: Session of the the first POST request
    :param link: The url of the page you want to request
    :return: <BeautifulSoup> The soup of the link that is passed in
    """
    res = session.get(link)
    soup = BeautifulSoup(res.text, 'html.parser')

    return soup


def show_all(soup):
    """
    Prints out the information of all articles in that page.

    :param soup: Soup of the page that you wan to parse
    """
    articles = soup.select('.r-ent')
    for index, article in enumerate(articles):
        print(f'---------- Article-{index} ----------')

        if article.find(class_='title').find('a'):
            print('標題:', article.find(class_='title').find('a').string)
            print('鏈結:', article.find(class_='title').find('a').get('href'))
        else:
            # The article has been deleted, so there is no link.
            print('標題:', article.find(class_='title').string.strip())

        print('作者:', article.find(class_='author').string)

        if article.find(class_='hl'):
            print('推文數:', article.find(class_='hl').string)
        else:
            print('尚無推文')

        print('日期:', article.find(class_='date').string)


def get_prev_plink(soup):
    """
    Returns the link of the previous page.

    :param soup: <BeautifulSoup> Soup of current page
    :return: <BeautifulSoup> Soup of the previous page in PTT
    """
    p_link = soup.select('.btn.wide')[1].get('href')
    prev_plink = PTT_ROOT + p_link

    return prev_plink


def make_article_dict(article):
    """
    Gathers all information of an article into a dictionary

    :param article: <bs4.element.Tag> The element that reprensents the article
    :return: <dict> A dictionary that contains all information of current article
    """
    dict_a = {}
    # Title and Link
    if article.select('.title > a'):
        dict_a['title'] = article.select('.title > a')[0].string
        dict_a['link'] = article.select('.title > a')[0].get('href')
    else:
        # The article has been deleted, so there is no link.
        dict_a['title'] = article.select('.title')[0].string.strip()
        dict_a['link'] = None
    # Author ID
    dict_a['author'] = article.select('.author')[0].string
    # Highlight
    if article.find(class_='hl'):
        dict_a['highlight'] = article.select('.hl')[0].string
    else:
        dict_a['highlight'] = '尚無推文'
    # Date
    dict_a['date'] = article.select('.date')[0].string

    return dict_a


def parse_info(soup):
    """
    Gathers all information of articles into a list of dictionaries.

    :param soup: <BeautifulSoup> Soup of current page
    :return: <List> A list of dictionaries that contains all information of current page
    """
    a_list = []

    # The first article
    article = soup.find(class_='r-ent')
    dict_article = make_article_dict(article)
    a_list.append(dict_article)

    # Detect the separate line to avoid the bottom articles
    while('r-list-sep' not in article.next_sibling.next_sibling.get('class')):
        article = article.next_sibling.next_sibling
        dict_article = make_article_dict(article)
        a_list.append(dict_article)

    return a_list


def show_json_list(articles):
    """
    A checking function that prints out the json-formatted list of articles
    """
    for a in articles:
        formatted = json.dumps(a, ensure_ascii=False, indent=4)
        print(formatted)

import json
import time

import requests
from bs4 import BeautifulSoup


def get_web_page(url):
    resp = requests.get(url=url, cookies={'over18': '1'})

    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None

    return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html5lib')

    # get the link of previous page
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for div in divs:
        if div.find('div', 'date').text.strip() == date:
            # get # of push
            push_count = 0
            push_str = div.find('div', 'nrec').text

            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            # get article link and title
            if div.find('a'):
                href = div.find('a')['href']
                title = div.find('a').text
                author = div.find('div', 'author').text if div.find('div', 'author') else ''
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count,
                    'author': author
                })

    return articles, prev_url


def main():
    print('start scraping from index page')
    current_page = get_web_page(PTT_URL + '/bbs/Beauty/index.html')

    if current_page:
        articles = []
        # today = time.strftime("%m/%d").lstrip('0')
        today = '6/19'
        current_articles, prev_url = get_articles(current_page, today)

        while current_articles:
            # articles += current_articles
            articles.extend(current_articles)
            print('moving to the previous page')
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, today)

        print('There are', len(articles), 'articles in PTT Gossiping')
        print('popular articles (> %d push)' % PUSH_THRESHOLD)

        for article in articles:
            if int(article['push_count']) > PUSH_THRESHOLD:
                print(article['push_count'], article['title'], article['author'], today,
                      ('%s%s' % (PTT_URL, article['href'])))

        with open('gossiping.json', 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    PTT_URL = 'https://www.ptt.cc'
    PUSH_THRESHOLD = 30
    main()

import requests
from bs4 import BeautifulSoup


def main():
    resp = requests.get('http://blog.castman.net/py-scraping-analysis-book/ch2/blog/blog.html')
    soup = BeautifulSoup(resp.text, 'html.parser')

    # find(): find the first element
    print(soup.find('h4'))
    # print(soup.h4)
    # print(soup.h4.a.text)

    # find_all(): find all elements
    main_titles = soup.find_all('h4', {'class': 'card-title'})
    for index, title in enumerate(main_titles):
        print(index, title.a.text)

    print(soup.find(id='mac-p'))

    print(soup.find(None, {'data-foo': 'mac-foo'}))

    # get all words for each blog
    divs = soup.find_all('div', 'content')
    for div in divs:
        # this will see line break
        # print(div.text)
        # use tag with strip to remove line break
        # print(div.h6.text.strip(), div.h4.a.text.strip(), div.p.text.strip())
        # use .stripped_strings
        print([s for s in div.stripped_strings])


if __name__ == '__main__':
    main()

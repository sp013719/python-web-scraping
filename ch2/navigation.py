import requests
from bs4 import BeautifulSoup


def main():
    resp = requests.get('http://blog.castman.net/py-scraping-analysis-book/ch2/table/table.html')
    soup = BeautifulSoup(resp.text, 'html.parser')
    prices = []

    # find price for all courses
    # approach 1
    # rows = soup.find('table', 'table').tbody.find_all('tr')
    # for row in rows:
    #     price = row.find_all('td')[2].text
    #     prices.append(int(price))

    # approach 2
    links = soup.find_all('a')
    for link in links:
        price = link.parent.previous_sibling.text
        prices.append(int(price))

    print('Total price: ', sum(prices)/len(prices))


if __name__ == '__main__':
    main()

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

    # get td values for each row of table
    rows = soup.find('table', 'table').tbody.find_all('tr')
    for index, row in enumerate(rows):
        # approach 1: find_all('td')
        # all_tds = row.find_all('td')
        # find the children of row
        all_tds = [td for td in row.children]

        if 'href' in all_tds[3].a.attrs:
            href = all_tds[3].a['href']
        else:
            href = None
        print(all_tds[0].text, all_tds[1].text, all_tds[2].text, href, all_tds[3].a.img['src'])
        print([s for s in row.stripped_strings])


if __name__ == '__main__':
    main()

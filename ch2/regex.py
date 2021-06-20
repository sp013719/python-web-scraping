import re
import requests
from bs4 import BeautifulSoup


def main():
    resp = requests.get('http://blog.castman.net/py-scraping-analysis-book/ch2/blog/blog.html')
    soup = BeautifulSoup(resp.text, 'html.parser')

    # find all titles
    titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for title in titles:
        print(title.text.strip())

    # find all titles by regular expression
    for title in soup.find_all(re.compile('h[1-6]')):
        print(title.text.strip())

    # find all images which file extension is .png
    images = soup.find_all('img')
    for img in images:
        if 'src' in img.attrs and img['src'].endswith('.png'):
            print(img['src'])

    # find all images by reg exp
    for img in soup.find_all('img', {'src': re.compile('\.png$')}):
        print('by reg: ', img['src'])

    # find image name which contains 'beginner' by reg exp
    for img in soup.find_all('img', {'src': re.compile('beginner.*\.png$')}):
        print('by reg: ', img['src'])


if __name__ == '__main__':
    main()

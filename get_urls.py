import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_content_website(page: int, data_dir='data'):
    if not os.path.exists(data_dir):
        try:
            os.mkdir(data_dir)
        except OSError as error:
            print(error)

    request = requests.get(f"https://www.dell.com/en-us/shop/gaming-gaming-accessories/ar/6488?page={page}")
    soup = BeautifulSoup(request.content, 'html.parser')
    with open(f"{data_dir}/website-page-{page}.html", 'w') as html_file:
        html_file.write(soup.prettify())

def get_urls(data_dir='data'):
    if os.path.exists('urls.txt'):
        os.remove('urls.txt')

    for page in tqdm(range(1, 27), desc="Getting URLs and witing it to urls.txt"):
        html_file = f"{data_dir}/website-page-{page}.html"
        if not os.path.exists(html_file):
            get_content_website(page)

        with open(html_file, 'r') as f:
            html_doc = f.read().rstrip()
        soup = BeautifulSoup(html_doc, 'html.parser')

        for section in soup.body.main.find_all('section', attrs={"class": "ps-top"}):
            for link in section.find_all('div', attrs={"class": "ps-image ps-snp-product-image"}):
                with open('urls.txt', 'a') as urls_file:
                    urls_file.write(f"https:{link.find('a').get('href')}\n")

if __name__ == "__main__":
    get_urls()

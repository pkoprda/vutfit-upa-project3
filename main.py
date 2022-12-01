import os
import requests
from bs4 import BeautifulSoup



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

    for page in range(1, 26):
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

def get_product_page(product_url):
    headers = {'content-type': 'application/json', 'user_agent': 'Mozilla/5.0'}
    product_url = product_url[:-1]
    request = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')
    
    product_name = soup.body.find('h1').span.contents[0].strip()
    product_price = soup.body.find('div', attrs={'class': "ps-dell-price ps-simplified"})
    try:
        product_price = product_price.find_all('span')[1].contents[0].strip()
    except:
        product_price = product_price.contents[0].strip()

    with open('data.tsv', 'a') as data_file:
            data_file.write(f"{product_url}\t{product_name}\t{product_price}\n")
    

def get_name_price():
    if os.path.exists('data.tsv'):
        os.remove('data.tsv')
    if not os.path.exists('urls.txt'):
        get_urls()

    with open("urls.txt", 'r') as f:
        lines = f.readlines()
        for product_url in lines:
            get_product_page(product_url)

if __name__ == "__main__":
    get_urls()
    get_name_price()

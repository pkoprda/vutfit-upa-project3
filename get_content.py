import requests
from bs4 import BeautifulSoup

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
    with open("urls.txt", 'r') as f:
        lines = f.readlines()
        for product_url in lines:
            get_product_page(product_url)

if __name__ == "__main__":
    get_name_price()
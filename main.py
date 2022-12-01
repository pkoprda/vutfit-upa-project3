import os

from get_urls import *
from get_content import *

if __name__ == "__main__":
    if os.path.exists('data.tsv'):
        os.remove('data.tsv')
    
    if not os.path.exists('urls.txt'):
        get_urls()
    
    get_name_price()
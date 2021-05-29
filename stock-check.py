import requests
import json
import time
import sys
from bs4 import BeautifulSoup

class bcolors:
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'

def currentTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

def print_out_stock():
    print(currentTime() + bcolors.FAIL + " OUT OF STOCK\t\t" + bcolors.ENDCOLOR, end = '- ')

def print_in_stock(price):
    print(currentTime() + bcolors.OK + " !!! IN STOCK:" + bcolors.ENDCOLOR, price, "\t", end = '- ')

def print_warn():
    print(currentTime() + bcolors.WARN + " COULDN'T CHECK" + bcolors.ENDCOLOR)

def countdown(seconds):
    for i in range(seconds, 0, -1):
        #I had to put some spaces in the end or the last char would be left everytime the string got smaller
        print("Checking again in", i, "seconds   ", end="\r", flush=True)
        time.sleep(1)

    print()

def get_cooldown():
    cooldown = 300
    if (len(sys.argv) > 1):
        if (int(sys.argv[1]) > 19 and int(sys.argv[1]) < 99999):
            cooldown = int(sys.argv[1])
        else:
            print("Invalid sleep interval. Cooldown set to 5 minutes.")

    return cooldown


def get_float_price(str):
    str = str.replace(" ", "")
    size = len(str)
    str = str[:size-3]
    str = str.replace("R$", "")
    str = str.replace(".", "")
    return float(str)

def get_amz_price(url):
    headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle")
    
    if (not title):
        print_warn()
        return

    title = title.get_text().strip()

    price = soup.find(id="priceblock_ourprice")

    if (not price):
        print_out_stock()
    else:
        price = price.get_text()
        price = get_float_price(price)
        print_in_stock(price)
    
    print(title)

def get_kbm_price(url):
    
    headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="titulo_det")
    if (not title):
        print_warn()
        return

    title = title.get_text().strip()
    is_sale = bool(soup.find(id="contador-cm"))

    if (is_sale):
        price = soup.find(class_="preco_desconto_avista-cm")

        if (not price):
            print_out_stock()
        else:
            price = price.get_text()
            price = get_float_price(price)
            print_in_stock(price)

    else:
        price = soup.find(class_="preco_desconto")

        if (not price):
            #When something is out of stock, a div with the alt text below is shown.
            price = soup.find(alt="produto_indisponivel")
            if (price):
                print_out_stock()
            else:
                print_warn()
        else:
            #Kabum stores many empty spaces and then more text inside the same element, so we take the first 15 digits(ignoring texts) and then strip the spaces
            price = price.get_text()[0:15].strip()
            price = get_float_price(price)
            print_in_stock(price)

    print(title)

def get_fastshop_price(url):
    headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.186 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    response = requests.get(url, headers = headers)
    jsonData = json.loads(response.content)
    title = jsonData['shortDescription']

    if (not jsonData['buyable']):
        print_out_stock()

    else:
        if (jsonData['priceOffer']):
            price = jsonData['priceOffer']
            print_in_stock(price)
        
        else:
            print_warn()
    
    print(title)

def get_fasts_api_url(link):
    #For fastshop, we can't scrape the info directly from page, so we get the product id and create an API Url to get data.
    fasts_pid = link.replace("https://www.fastshop.com.br/web/p/d/", "")
    fasts_pid = fasts_pid.split("/", 1)[0]
    link = 'https://www.fastshop.com.br/wcs/resources/v5/products/byPartNumber/'+fasts_pid
    return link




cooldown = get_cooldown()

f = open("urls.txt", "r")
url_list = f.readlines()
amz_links = []
kbm_links = []
fst_links = []

for url in url_list:
    if('amazon.com' in url):
        amz_links.append(url)
    elif ('kabum.com.br' in url):
        kbm_links.append(url)
    elif ('fastshop.com.br' in url):
        url = get_fasts_api_url(url)
        fst_links.append(url)
    else:
        print("Invalid URL. Ignoring.")

while (True):
    for amz_url in amz_links:
        get_amz_price(amz_url)

    for kbm_url in kbm_links:
        get_kbm_price(kbm_url)

    for fst_url in fst_links:
        get_fastshop_price(fst_url)

    countdown(cooldown)


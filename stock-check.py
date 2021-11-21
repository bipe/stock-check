import requests
import json
import time
import sys
import utils
from bs4 import BeautifulSoup

def get_cooldown():
    cooldown = 300
    if (len(sys.argv) > 1):
        if (int(sys.argv[1]) > 19 and int(sys.argv[1]) < 99999):
            cooldown = int(sys.argv[1])
        else:
            print("Invalid sleep interval. Cooldown set to 5 minutes.")

    return cooldown

def getAmzPriceElement(soup):
    price = soup.find(class_="a-text-price")
    if (not price):
        return
    price = price.find(class_="a-offscreen")
    return price

def get_amz_price(url):
    headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle")
    
    if (not title):
        utils.print_warn('title not found')
        return

    title = title.get_text().strip()

    price = getAmzPriceElement(soup)
    if (not price):
        utils.print_out_stock()
    else:
        price = price.get_text()
        price = utils.str_to_float_price(price)
        utils.print_in_stock(price)
    
    print(title)

def get_kbm_price(url):
    
    headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("h1")
    if (not title):
        utils.print_warn()
        return

    title = title.get_text(strip=True)
    is_sale = bool(soup.find(id="contador-cm"))

    if (is_sale):
        price = soup.find(class_="preco_desconto_avista-cm")

        if (not price):
            utils.print_out_stock()
        else:
            price = price.get_text()
            price = utils.str_to_float_price(price)
            utils.print_in_stock(price)

    else:
        price = soup.find(class_="preco_desconto")

        if (not price):
            #When something is out of stock, a div with the id below is shown.
            price = soup.find(id="formularioProdutoIndisponivel")
            if (price):
                utils.print_out_stock()
            else:
                utils.print_warn()
        else:
            #Kabum stores many empty spaces and then more text inside the same element, so we take the first 15 digits(ignoring texts) and then strip the spaces
            price = price.get_text()[0:15].strip()
            price = utils.str_to_float_price(price)
            utils.print_in_stock(price)

    print(title)

def get_fastshop_price(url):
    headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.186 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    response = requests.get(url, headers = headers)
    jsonData = json.loads(response.content)

    if ('errorMessage' in jsonData):
        utils.print_warn(jsonData['errorMessage'])
        return

    title = jsonData['shortDescription']

    if (not jsonData['buyable']):
        utils.print_out_stock()

    else:
        if (jsonData['priceOffer']):
            price = jsonData['priceOffer']
            utils.print_in_stock(price)
        
        else:
            utils.print_warn()
    
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

    utils.countdown(cooldown)


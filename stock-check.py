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


def print_out_stock():
    print(bcolors.FAIL + "OUT OF STOCK\t\t" + bcolors.ENDCOLOR, end = '- ')

def print_in_stock(price):
    print(bcolors.OK + "!!! IN STOCK:" + bcolors.ENDCOLOR, price, "\t", end = '- ')

def print_warn():
    print(bcolors.WARN + "COULDN'T CHECK" + bcolors.ENDCOLOR, end = '- ')

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

    title = soup.find(id="productTitle").get_text().strip()
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

    title = soup.find(id="titulo_det").get_text().strip()
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


#available product URL for testing (not in sale):
#'https://www.kabum.com.br/produto/69306/c-mbio-logitech-g-driving-force-compat-vel-com-volantes-logitech-g29-e-g920-para-ps4-xbox-one-e-pc-941-000119'
kbm_url = 'https://www.kabum.com.br/produto/115737/console-sony-playstation-5-cfi-1014a'

#available product URL for testing:
#'https://www.amazon.com.br/Microsoft-Console-Xbox-Series-S/dp/B08JN2VMGX/ref=pd_sbs_5/140-4748579-5457636'
amz_url = 'https://www.amazon.com.br/dp/B088GNRX3J/ref=s9_acss_bw_cg_HeroVG_1a1_w'

#available product URL for testing (dual schock 4):
#https://www.fastshop.com.br/wcs/resources/v5/products/byPartNumber/SO3004192AZL_PRD
#For fastshop, you have to take the API url to get product
fastshop_url = 'https://www.fastshop.com.br/wcs/resources/v5/products/byPartNumber/SO3005724BCOB'

cooldown = get_cooldown()

while (True):
    get_amz_price(amz_url)
    get_kbm_price(kbm_url)
    get_fastshop_price(fastshop_url)
    countdown(cooldown)


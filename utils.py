import time

class bcolors:
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'

def str_to_float_price(str):
    str = str.replace(" ", "")
    size = len(str)
    str = str[:size-3]
    str = str.replace("R$", "")
    str = str.replace(".", "")
    return float(str)

def current_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

def print_out_stock():
    print(current_time() + bcolors.FAIL + " OUT OF STOCK\t\t" + bcolors.ENDCOLOR, end = '- ')

def print_in_stock(price):
    print(current_time() + bcolors.OK + " !!! IN STOCK:" + bcolors.ENDCOLOR, price, "\t", end = '- ')

def print_warn(exception = None):
    if (exception):
        print(current_time() + bcolors.WARN + " COULDN'T CHECK\t\t" + bcolors.ENDCOLOR + " - " + exception)
        return

    print(current_time() + bcolors.WARN + " COULDN'T CHECK" + bcolors.ENDCOLOR)

def countdown(seconds):
    for i in range(seconds, 0, -1):
        #I had to put some spaces in the end or the last char would be left everytime the string got smaller
        print("Checking again in", i, "seconds   ", end="\r", flush=True)
        time.sleep(1)

    print()

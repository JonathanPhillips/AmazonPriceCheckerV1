import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import csv

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

bucket_list = ['https://www.amazon.com/Forever-Story-2-LP/dp/B0BJQDGS3S/',
               'https://www.amazon.com/GHETTO-GODS-Black-Gold-Swirl/dp/B0BFBY8C3Y/',
               'https://www.amazon.com/gp/product/B0B7XY3JN6/',
               'https://www.amazon.com/Can-Take-My-Hounds-Heaven/dp/B0BDMPPLJX/',
               'https://www.amazon.com/Daytona-PUSHA-T/dp/B07DQ321CK/',
               'https://www.amazon.com/Ctrl-SZA/dp/B0765CCMW9/',
               'https://www.amazon.com/Dawn-FM-2-LP-Weeknd/dp/B09PP8QPTZ/',

                ]

def get_amazon_price(dom):

    try:
        #price = soup.find(name="span", class_="a-offscreen").getText()
        #price = WebDriverWait(browser,10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='a-offscreen']/text()")))
        #price = soup.find(id="tp_price_block_total_price_ww")
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        #fraction = dom.xpath('//span[@class="a-price-fraction"]/text()')[0]
        price = price.replace('$', '')
        return price
    except Exception as e:
        price = 'Not Available'
        return None


def get_product_name(dom):
    try:
        name = dom.xpath('//span[@id="productTitle"]/text()')
        [name.strip() for name in name]
        return name[0]
    except Exception as e:
        name = 'Not Available'
        return None

# write data into a csv file

with open('master_data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['product name', 'price', 'url'])

    for url in bucket_list:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')
        amazon_dom = et.HTML(str(soup))
  
        

        product_name = get_product_name(amazon_dom)
        product_price = get_amazon_price(amazon_dom)

        time.sleep(random.randint(2, 10))

        writer.writerow([product_name, product_price, url])
        print(product_name, product_price, url)

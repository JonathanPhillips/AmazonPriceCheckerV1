import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import pandas as pd
from twilio.rest import Client
import sys

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

amazon_urls = ['https://www.amazon.com/Forever-Story-2-LP/dp/B0BJQDGS3S/',
               'https://www.amazon.com/GHETTO-GODS-Black-Gold-Swirl/dp/B0BFBY8C3Y/',
               'https://www.amazon.com/gp/product/B0B7XY3JN6/'
                ] 

def get_amazon_price(dom):
    item_price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
    item_price = item_price.replace('$', '')
    return float(item_price)

def get_product_name(dom):
    name = dom.xpath('//span[@id="productTitle"]/text()')
    [name.strip() for name in name]
    return name[0]

def get_master_price(url):
    for row in df.itertuples():
        if row.url == url:
            return row.price
    return None  


price_drop_products = []
price_drop_list_url = []

for product_url in amazon_urls:

    response = requests.get(product_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_dom = et.HTML(str(soup))

    price = get_amazon_price(main_dom)
    product_name = get_product_name(main_dom)
    df = pd.read_csv('master_data.csv')

    if price < get_master_price(product_url):
        change_percentage = round((get_master_price(product_url) - price) * 100 / get_master_price(product_url))

        if change_percentage > 10:
            print(' There is a {}'.format(change_percentage), '% drop in price for {}'.format(product_name))
            print('Click here to purchase {}'.format(product_url))
            price_drop_products.append(product_name)
            price_drop_list_url.append(product_url)

if len(price_drop_products) == 0:
    sys.exit('No Price drop found')

message = "There is a drop in price for {}".format(len(price_drop_products)) + " products." + "Click to purchase"

for items in price_drop_list_url:
    message = message + "\n" + items

account_sid = 'YOURSID'
auth_token = 'YOURTOKEN'

client = Client(account_sid, auth_token)
message = client.messages.create(
    from_='Your twilio phone number',
    body=message,
    to='Your personal mobile number'
)

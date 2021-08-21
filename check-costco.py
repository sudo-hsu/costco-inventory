import time
from bs4 import BeautifulSoup
import requests
from discord import Webhook, RequestsWebhookAdapter, Embed
import secrets

def get_page_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    page = requests.get(url, headers=headers)
    return page.content

def item_name(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    name = soup.h1.string
    return name

def check_item_in_stock(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    out_of_stock_divs = soup.findAll("img", {"class": "oos-overlay hide"})
    return len(out_of_stock_divs) != 0

def send_to_discord(page_html, url):
    webhook = Webhook.from_url(secrets.DISCORD, adapter=RequestsWebhookAdapter())
    embed = Embed(title=item_name(page_html) + " is in stock!")
    embed.description = url
    webhook.send(embed=embed)

def check_inventory():
    #url = "https://www.costco.com/nba-2k21---playstation-5-game.product.100725581.html"
    url = "https://www.costco.com/sony-playstation-5-gaming-console-bundle.product.100691489.html"
    page_html = get_page_html(url)
    if check_item_in_stock(page_html):
        send_to_discord(page_html, url)
        print(item_name(page_html) + " is in stock!")
    else:
        print(item_name(page_html) + " is out of stock still.")

while True:
    check_inventory()
    time.sleep(300)  # Wait 5 minutes and try again

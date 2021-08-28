#!/usr/local/bin/python3
import urllib.request, json
import smtplib
import traceback
import urllib.request
from bs4 import BeautifulSoup
import re
import os, sys
import requests

#links
json_NBU_api = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
url_GoogleFinance_CDPROJEKT = urllib.request.urlopen("https://www.google.com/finance/quote/CDR:WSE")
url_GoogleFinance_BTC = urllib.request.urlopen("https://www.google.com/finance/quote/BTC-USD")
url_GoogleFinance_ETH = urllib.request.urlopen("https://www.google.com/finance/quote/ETH-USD")
url_GoogleFinance_XRP = urllib.request.urlopen("https://www.google.com/finance/quote/XRPLX:INDEXNASDAQ")

#main variables
USD_UAH_price = 0
EUR_UAH_price = 0
PLN_UAH_price = 0
CDPROJEKT_price = 0
BTC_price = 0
ETH_price = 0
XRP_price = 0

def Get_ExchangeRate():
    #Get data from NBU API
    global USD_UAH_price, EUR_UAH_price, PLN_UAH_price
    with urllib.request.urlopen(json_NBU_api) as url:
        data = json.loads(url.read().decode())
    USD_UAH_price = data[26]["rate"]
    print(USD_UAH_price)
    EUR_UAH_price = data[32]["rate"]
    print(EUR_UAH_price)
    PLN_UAH_price = data[33]["rate"]
    print(PLN_UAH_price)

def Get_CDPROJECT_stocks():
    #Get data from Google Finance 
    global CDPROJEKT_price
    soup = BeautifulSoup(url_GoogleFinance_CDPROJEKT)
    CDPROJEKT_price = soup.find_all("div", {"class": "YMlKec fxKbKc"})
    CDPROJEKT_price = ''.join(re.findall('\d+.\d+', str(CDPROJEKT_price)))
    print(CDPROJEKT_price)

def Get_Crypto_price():
    #Get data from Google Finance
    global BTC_price, ETH_price, XRP_price
    soup = BeautifulSoup(url_GoogleFinance_BTC)
    BTC_price = soup.find_all("div", {"class": "YMlKec fxKbKc"})
    BTC_price = ''.join(re.findall('\d+,\d+.\d+', str(BTC_price)))
    soup = BeautifulSoup(url_GoogleFinance_ETH)
    ETH_price = soup.find_all("div", {"class": "YMlKec fxKbKc"})
    ETH_price = ''.join(re.findall('\d+,\d+.\d+', str(ETH_price)))
    soup = BeautifulSoup(url_GoogleFinance_XRP)
    XRP_price = soup.find_all("div", {"class": "YMlKec fxKbKc"})
    XRP_price = ''.join(re.findall('\d+.\d+', str(XRP_price)))
    print(BTC_price, ETH_price, XRP_price)

def Send_Telegram_bot_message():
    #Prepare message to send by bot
    message_to_send = """
    Exchange Rates:\n\nUSD: {} грн\nEUR: {} грн\nPLN: {} грн\n\n₿:\n{} $\n\nETH:\n{} $\n\nXRP:\n{} $\n\nCD Project price: \n{} zł\n
    """.format(USD_UAH_price, EUR_UAH_price, PLN_UAH_price, BTC_price, ETH_price, XRP_price, CDPROJEKT_price)
    #Get bot token and chat id from .txt files
    with open(os.path.join(sys.path[0],'bot_token.txt'), 'r') as file:
        bot_token = file.read().rstrip('\n')
    with open(os.path.join(sys.path[0],'chat_id.txt'), 'r') as file:
        chat_id = file.read().rstrip('\n')
    base_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_token, chat_id, message_to_send)
    #Send message
    requests.get(base_url)

def main():
    Get_ExchangeRate()
    Get_CDPROJECT_stocks()
    Get_Crypto_price()
    Send_Telegram_bot_message()

if __name__ == "__main__":
    main()
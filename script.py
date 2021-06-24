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
api_json_monobank_ExchangeRates = "https://api.monobank.ua/bank/currency"
url_GPW_CDPROJEKT = urllib.request.urlopen("https://www.gpw.pl/spolka?isin=PLOPTTC00011")
url_Google_BTC = urllib.request.urlopen("https://www.google.com/finance/quote/BTC-USD")
url_Google_ETH = urllib.request.urlopen("https://www.google.com/finance/quote/ETH-USD")

#main variables
ExchangeRates = ""
CDPROJEKT_stocks = ""
BTC_price = ""
ETH_price = ""

def Get_ExchangeRate():
    #Get data from mono API
    with urllib.request.urlopen(api_json_monobank_ExchangeRates) as url:
        data_exRates_mono = json.loads(url.read().decode())
    UAH_USD_Buy_mono = data_exRates_mono[0]["rateBuy"]      #USD
    UAH_USD_Sell_mono = data_exRates_mono[0]["rateSell"]
    UAH_EUR_Buy_mono = data_exRates_mono[1]["rateBuy"]      #EUR
    UAH_EUR_Sell_mono = data_exRates_mono[1]["rateSell"]
    global ExchangeRates
    ExchangeRates = "USD: " + str(UAH_USD_Buy_mono) + " грн. / " + str(UAH_USD_Sell_mono) + " грн.\nEUR:  " + str(UAH_EUR_Buy_mono) + " грн. / " + str(UAH_EUR_Sell_mono) + " грн.\n\n" 
    #print(ExchangeRates)

def Get_CDPROJECT_stocks():
    #Get CDProject stocks
    soup = BeautifulSoup(url_GPW_CDPROJEKT)
    CDPROJEKT_results = soup.find('table', {"table table-borderLess table-sm font18 margin-bottom-0"}).findAll('tr')
    CDPROJEKT_bid = re.search('\d+.\d+', str(CDPROJEKT_results[0])).group(0)    #oferta kupna
    CDPROJEKT_ask = re.search('\d+.\d+', str(CDPROJEKT_results[1])).group(0)    #oferta sprzeday
    global CDPROJEKT_stocks 
    CDPROJEKT_stocks = '{} zł / {} zł'.format(CDPROJEKT_bid, CDPROJEKT_ask)
    #print(CDPROJEKT_stocks)

def Get_Crypto_price():
    #Get Crypto price
    soup = BeautifulSoup(url_Google_BTC)
    global BTC_price
    BTC_price = soup.findAll("div", class_="YMlKec fxKbKc")
    BTC_price = re.search('\d+,\d+', str(BTC_price[0])).group(0) + " $"
    soup = BeautifulSoup(url_Google_ETH)
    global ETH_price
    ETH_price = soup.findAll("div", class_="YMlKec fxKbKc")
    ETH_price = re.search('\d+,\d+', str(ETH_price[0])).group(0) + " $"

def Send_email(sent_to):
    #Get mail_user and mail_password from .txt files to send email
    with open(os.path.join(sys.path[0],'mail_user.txt'), 'r') as file:
        mail_user = file.read().rstrip('\n')
    with open(os.path.join(sys.path[0],'mail_password.txt'), 'r') as file:
        mail_password = file.read().rstrip('\n')
    #Define mail message
    sent_from = mail_user
    subject = "Exchange Rates"
    text = ExchangeRates
    message = """\
    From: %s
    To: %s
    Subject: %s
    
    %s
    """ % (sent_from, ", ".join(sent_to), subject, text)
    #Sending mail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mail_user, mail_password)
        server.sendmail(sent_from, sent_to, message)
        server.quit()
    except:
        traceback.print_exc()
        print('Something went wrong...')

def Send_Telegram_bot_message():
    #Prepare message to send by bot
    message_to_send = """
    🇺🇦\n{}🦜\n{}\n\n₿:\n{}\n\nETH:\n{}\n\n
    """.format(ExchangeRates, CDPROJEKT_stocks, BTC_price, ETH_price)
    #Get bot token and chat id from .txt files
    with open(os.path.join(sys.path[0],'bot_token.txt'), 'r') as file:
        bot_token = file.read().rstrip('\n')
    with open(os.path.join(sys.path[0],'chat_id.txt'), 'r') as file:
        chat_id = file.read().rstrip('\n')
    base_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_token, chat_id, message_to_send)
    requests.get(base_url)

def main():
    Get_ExchangeRate()
    Get_CDPROJECT_stocks()
    Get_Crypto_price()
    Send_Telegram_bot_message()

if __name__ == "__main__":
    main()
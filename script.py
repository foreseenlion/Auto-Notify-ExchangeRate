#!/usr/local/bin/python3
import urllib.request, json
import smtplib
import traceback
import urllib.request
from bs4 import BeautifulSoup
import re
import os, sys

#links
api_json_monobank_ExchangeRates = "https://api.monobank.ua/bank/currency"
url_GPW_CDPROJEKT = urllib.request.urlopen("https://www.gpw.pl/spolka?isin=PLOPTTC00011")

#get data from mono API
with urllib.request.urlopen(api_json_monobank_ExchangeRates) as url:
    data_exRates_mono = json.loads(url.read().decode())

#USD
UAH_USD_Buy_mono = data_exRates_mono[0]["rateBuy"]
UAH_USD_Sell_mono = data_exRates_mono[0]["rateSell"]
#EUR
UAH_EUR_Buy_mono = data_exRates_mono[1]["rateBuy"]
UAH_EUR_Sell_mono = data_exRates_mono[1]["rateSell"]

#print("   UAH - USD  BUY     :   ", UAH_USD_Buy_mono)
#print("   UAH - USD  SELL    :   ", UAH_USD_Sell_mono)
#print("   UAH - EUR  BUY     :   ", UAH_EUR_Buy_mono)
#print("   UAH - EUR  SELL    :   ", UAH_EUR_Sell_mono)

ExchangeRates = "\n\nUSD: " + str(UAH_USD_Buy_mono) + " / " + str(UAH_USD_Sell_mono) + "  EUR:  " + str(UAH_EUR_Buy_mono) + " / " + str(UAH_EUR_Sell_mono) + "\n\n" 
print(ExchangeRates)


#CDProject factssheet
soup = BeautifulSoup(url_GPW_CDPROJEKT)
CDPROJEKT_results = soup.find('table', {"table table-borderLess table-sm font18 margin-bottom-0"}).findAll('tr')
CDPROJEKT_bid = re.search('\d+.\d+', str(CDPROJEKT_results[0])).group(0)    #oferta kupna
CDPROJEKT_ask = re.search('\d+.\d+', str(CDPROJEKT_results[1])).group(0)    #oferta sprzeday


#TODO unique path to gmail_user.txt and gmail_password.txt
#Get gmail_user and gmail_password to send mail message
with open(os.path.join(sys.path[0],'gmail_user.txt'), 'r') as file:
    gmail_user = file.read().rstrip('\n')
with open(os.path.join(sys.path[0],'gmail_password.txt'), 'r') as file:
    gmail_password = file.read().rstrip('\n')


#Define mail message
sent_from = gmail_user
sent_to = ['rysanov.leonid@mail.ru']
subject = "Exchange Rates"
text = ExchangeRates
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(sent_to), subject, text)


"""
#sending mail
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, sent_to, message)
    server.quit()
except:
    traceback.print_exc()
    print('Something went wrong...')
"""


#BASH Commands for communitation between Mac and Raspberry Pi

# Copy repo from Mac to Raspberry Pi  
#   sshpass -f "pass_to_pi" scp -r NotifyMail-ExchangeRate+Stocks pi@192.168.0.122:/home/pi
# Log to Raspberry Pi and delete repo
#   sshpass -f "pass_to_pi" ssh pi@192.168.0.122 "rm -r NotifyMail-ExchangeRate+Stocks"

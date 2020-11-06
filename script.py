#!/usr/local/bin/python3
import urllib.request, json
import smtplib
import traceback
import urllib.request
from bs4 import BeautifulSoup
import re

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

print("   UAH - USD  BUY     :   ", UAH_USD_Buy_mono)#
print("   UAH - USD  SELL    :   ", UAH_USD_Sell_mono)
print("   UAH - EUR  BUY     :   ", UAH_EUR_Buy_mono)
print("   UAH - EUR  SELL    :   ", UAH_EUR_Sell_mono)

ExchangeRates = "USD: " + str(UAH_USD_Buy_mono) + "/" + str(UAH_USD_Sell_mono) + "  EUR:  " + str(UAH_EUR_Buy_mono) + "/" + str(UAH_EUR_Sell_mono) 
print(ExchangeRates)

#TODO unique path to gmail_user.txt and gmail_password.txt
#Get gmail_user and gmail_password to send mail message
with open('/Users/leonidrusanov/Documents/automation_scripts/Auto-Notify-ExchangeRate/gmail_user.txt', 'r') as file:
    gmail_user = file.read().rstrip('\n')
with open('/Users/leonidrusanov/Documents/automation_scripts/Auto-Notify-ExchangeRate/gmail_password.txt', 'r') as file:
    gmail_password = file.read().rstrip('\n')
    
sent_from = gmail_user
sent_to = ['rysanov.leonid@mail.ru']

subject = ExchangeRates
text = ExchangeRates


#CDPROJECT FACTSSHEET

soup = BeautifulSoup(url_GPW_CDPROJEKT)
#print(soup.prettify())
CDPROJEKT_results = soup.find('table', {"table table-borderLess table-sm font18 margin-bottom-0"}).findAll('tr')
CDPROJEKT_bid = re.search('\d+.\d+', str(CDPROJEKT_results[0])).group(0)
CDPROJEKT_ask = re.search('\d+.\d+', str(CDPROJEKT_results[1])).group(0)

#DEFINE MAIL MESSAGE
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(sent_to), subject, text)


try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, sent_to, message)
    server.quit()
except:
    traceback.print_exc()
    print('Something went wrong...')

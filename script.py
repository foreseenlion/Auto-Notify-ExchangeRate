import urllib.request, json
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

api_json_monobank_ExchangeRates = "https://api.monobank.ua/bank/currency"

#get data from mono API
with urllib.request.urlopen(api_json_monobank_ExchangeRates) as url:
    data_exRates_mono = json.loads(url.read().decode())

#USD
UAH_USD_Buy_mono = data_exRates_mono[0]["rateBuy"]
UAH_USD_Sell_mono = data_exRates_mono[0]["rateSell"]
#EUR
UAH_EUR_Buy_mono = data_exRates_mono[1]["rateBuy"]
UAH_EUR_Sell_mono = data_exRates_mono[1]["rateSell"]

print("   UAH - USD  BUY     :   ", UAH_USD_Buy_mono)
print("   UAH - USD  SELL    :   ", UAH_USD_Sell_mono)
print("   UAH - EUR  BUY     :   ", UAH_EUR_Buy_mono)
print("   UAH - EUR  SELL    :   ", UAH_EUR_Sell_mono)

ExchangeRates = "USD: " + str(UAH_USD_Buy_mono) + "/" + str(UAH_USD_Sell_mono) + "  EUR:  " + str(UAH_EUR_Buy_mono) + "/" + str(UAH_EUR_Sell_mono) 
print(ExchangeRates)

#TODO
with open('gmail_user.txt', 'r') as file:
    gmail_user = file.read().rstrip('\n')
with open('gmail_password.txt', 'r') as file:
    gmail_password = file.read().rstrip('\n')
    
sent_from = gmail_user
sent_to = ['rysanov.leonid@mail.ru']

subject = ExchangeRates
text = ExchangeRates

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(sent_to), subject, text)

#msg.attach(MIMEText('cos', 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, sent_to, message)
    server.quit()
except:
    traceback.print_exc()
    print('Something went wrong...')

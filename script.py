import urllib.request, json
import smtplib

api_json_monobank_ExchangeRates = "https://api.monobank.ua/bank/currency"

#get data from mono API
with urllib.request.urlopen(api_json_monobank_ExchangeRates) as url:
    data_exRates_mono = json.loads(url.read().decode())

UAH_USD_Buy_mono = data_exRates_mono[0]["rateBuy"]
UAH_USD_Sell_mono = data_exRates_mono[0]["rateSell"]
UAH_EUR_Buy_mono = data_exRates_mono[1]["rateBuy"]
UAH_EUR_Sell_mono = data_exRates_mono[1]["rateSell"]

print("   UAH - USD  BUY     :   ", UAH_USD_Buy_mono)
print("   UAH - USD  SELL    :   ", UAH_USD_Sell_mono)
print("   UAH - EUR  BUY     :   ", UAH_EUR_Buy_mono)
print("   UAH - EUR  SELL    :   ", UAH_EUR_Sell_mono)

#TODO
gmail_user = 'mail to create'
gmail_password = 'password to create'

sent_from = gmail_user
to = ['rysanov.leonid@mail.ru']
subject = 'OMG Super Important Message'
body = 'Hey, what\'s up?\n\n- You'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
except:
    print('Something went wrong...')
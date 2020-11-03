import urllib.request, json

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





        








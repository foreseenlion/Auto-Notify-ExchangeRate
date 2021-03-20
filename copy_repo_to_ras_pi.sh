#!/bin/bash
echo ""
echo Delete repo from Rasberry Pi:
echo ""
sshpass -f "pass_to_pi" ssh pi@192.168.0.122 "rm -r NotifyMail-ExchangeRate+Stocks" | pv
echo ""
echo Delete completed
echo ""
echo Copy repo to Rasberry Pi
echo ""
sshpass -f "pass_to_pi" scp -r NotifyMail-ExchangeRate+Stocks pi@192.168.0.122:/home/pi | pv
echo ""
echo Copy completed
echo ""

#TODO
#check if commands fails
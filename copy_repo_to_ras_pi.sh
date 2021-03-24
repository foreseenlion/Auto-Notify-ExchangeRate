#!/bin/bash
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
echo Delete repo from Raspberry Pi:
echo ""
if (sshpass -f "pass_to_pi" ssh pi@192.168.0.122 "rm -r TelegramBot-ExchangeRate+Stocks" | pv); then
    echo -e "${GREEN}Delete completed successfully${NC}"
else
    echo -e "${RED}Delete faild${NC}"
fi
echo ""
echo Copy repo to Raspberry Pi
echo ""
if (sshpass -f "pass_to_pi" scp -r NotifyMail-ExchangeRate+Stocks pi@192.168.0.122:/home/pi | pv); then
    echo -e "${GREEN}Copy completed successfully${NC}"
else
    echo -e "${GREEN}Copy faild${NC}"
fi
echo ""

# etsyLowInventoryCheck
Lightweight application to periodically check each Etsy listing in your shop and send an email if a particular variant in a listing is low in stock.

## Purpoose
Never run low on your Etsy shop's inventory again! Stay in the know when each individual listing's variations runs low with an email sent to your inbox.

## Getting Started
1. Fill in variable data in `config.py`
2. On your Linux server, edit your cron using `crontab -e`
3. Add the line `@reboot python3 ~/etsyLowInventoryCheck/app.py` and save changes
4. Reboot server with `reboot` 

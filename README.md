### Magic Script
A simple Python script to fetch, store and analize the MTG cards price
over time using external API
This script use the API Provided by [Scryfall](scryfall.com) and [CardTrader](https://www.cardtrader.com/)

Scryfall API are used to fetch the card information such as card code, edition, ecc...

CardTrader API are used to fetch the card prices, availability an stock statistic

## Install
Be sure to have a CardTrader login token before running the script
Export your token inside the terminal or set it in your environment if you want
to automathe the execution of the script, eg:
```
export AUTH_TOKEN="<your token>"
```

Configure the script using the `--config` option:
```
$ python main.py --config
```
The config proceedure walk you through the various steps and after you have finished with it
you can proceed with the execution of the script core

In alternative you can provide a `.yaml` file with your desired configuration
## Usage
Simply execute the `main.py` file with Pythone
```
$ python main.py
```
If you have set the script configuration with the default value you should find a PDF
file with the card information in your home directory `\home\username` named `PriceReport.pdf`

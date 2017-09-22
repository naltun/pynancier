#!/usr/bin/env python

# Pynancier is a Python script for delivering real-time, up-to-date Cryptocurrency market data
# Pynancier is a portmanteau of *Python* and *Financier*
#
# INTENDED USE:
# I intend to run this in tmux, in its own tile, so I can glance over from time-to-time. Feel free to use your imagination and to find new ways to enjoy it
#
# This script may grow in functionality as is seen fit, or may not
#
# Licensed proudly under the the GNU General Public License Version 2
# For information regarding Free/Libre software, please read more at en.wikipedia.org/wiki/Free_software
# Happy coding
#
# Developed by Noah Altunian (github.com/naltun)

# our only 3rd party dependency is Requests - it can be installed using the `pip' or `pipenv'command-line tool
import requests
import sys
import time
from subprocess import call

version = '0.2.0-beta.1'

# Pynancier ASCII logo; made with figlet.js (github.com/patorjk/figlet.js)
logo = """  _____                              _
 |  __ \                            (_)
 | |__) |   _ _ __   __ _ _ __   ___ _  ___ _ __
 |  ___/ | | | '_ \ / _` | '_ \ / __| |/ _ \ '__|
 | |   | |_| | | | | (_| | | | | (__| |  __/ |
 |_|    \__, |_| |_|\__,_|_| |_|\___|_|\___|_| v%s
         __/ |
        |___/
""" % (version)

# where we're actually getting our information from
global_data_url = 'https://api.coinmarketcap.com/v1/global/'

# clear screen function -- simply executes `clear' in the shell
def clear_screen():
    call('clear')

# check to see if we are supplied a command-line, numerical argument; if so, work some extra magic
# (eg. display info on the top argv[1] cryptocurrencies)
arg = int(sys.argv[1])
if bool(arg):
    # Currently Pynancier will only support up to 6 cryptocurrencies (ergo, a maximum argument size of 6)
    if arg <= 6:
        ticker_limit = arg
    else:
        ticker_limit = 6

    ticker_url = 'https://api.coinmarketcap.com/v1/ticker/?limit=' + str(ticker_limit)

    def get_currency_data():
        currency_data_raw = requests.get(ticker_url)
        currency_data     = currency_data_raw.json()

        for currency in currency_data:
            print("Currency:   %s"  % currency['name'])
            print("Symbol:     %s"  % currency['symbol'])
            print("Rank:       %s"  % currency['rank'])
            print("Price (USD) $%s" % '{0:,}'.format(currency['price_usd']))

# get the data, then the girl
def get_global_data():
    # response returns data as JSON, but we need to convert it from returned input -> JSON we can use
    global_data_raw  = requests.get(global_data_url)
    global_data      = global_data_raw.json()

    # let's format that exceptionally large number to include commas, shall we?
    total_market_cap  = '{0:,}'.format(global_data['total_market_cap_usd'])
    bitcoin_dominance = global_data['bitcoin_percentage_of_market_cap']
    active_currencies = global_data['active_currencies']

    print("Total Market Cap:        $%s" % total_market_cap)
    print("Bitcoin Dominance:       %s"  % bitcoin_dominance)
    print("Total Active Currencies: %s"  % active_currencies)

# patience is a virtue -- here it allows the script to cease making any additional web requests for 60 seconds so I can read the darn data
def wait():
    time.sleep(60)

# let's do this
while True:
    clear_screen()
    print(logo)
    get_global_data()
    try:
        # print blank lines for cleanliness
        print()
        get_currency_data()
        print()
    except:
        # Do nothing -- leave the loop cleanly
        pass
    wait()

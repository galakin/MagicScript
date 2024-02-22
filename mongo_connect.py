import requests
import os
import pathlib
import pandas
import json
import argparse
import sys
import yaml
import pymongo

import src.priceCard as priceCard
import src.rwCsw as rwCsw
import src.connection as nwrk

import src.pdfManipulation as pdf
import src.exceptions as expt
import global_var
import src.check_csv as check_csv


def fetch_local_card_data():
    client = pymongo.MongoClient()
    dbnames = client.list_database_names()

    if "cards" in dbnames:
        print("...cards db found")
    else:
        print("...Unable to find cards db")
        cards_db = client["cards"]
        mycol = cards_db["cards_data"]

        # Import cards from cards.csv file
        home_dir = os.getenv("HOME")
        if home_dir == None:
            raise expt.InternalException(
                "Unable to find environment variable named HOME\nplease check if you have defined it"
            )
            return False

        mydict = {"name": "tst", "address": "Highway 37"}

    print(dbnames)


#    home_dir = os.getenv("HOME")
#    if home_dir == None:
#        raise expt.InternalException(
#            "Unable to find environment variable named HOME\nplease check if you have defined it"
#        )
#        return False
#
#    price_csv = pathlib.Path(global_var.custom_dir + "/price.csv")
#    file_path = pathlib.Path(home_dir + "/card.csv")
#    if file_path.is_file():
#        print("Card file found!")
#    else:
#        raise expt.InternalException(
#            "Unable to fin the card file a the default location!"
#        )
#        return False
#    if price_csv.is_file():
#        print("... card price csv file found!")
#    else:
#        price_csv = open(global_var.custom_dir + "/price.csv", "x")
#        price_csv.writelines(
#            [
#                "name,exp,min_price,max_price,mean_price,foil_min_price,foil_max_price,foil_mean_price,signed_min_price,signed_max_price,signed_mean_price,altered_min_price,altered_max_price,altered_mean_price\n"
#            ]
#        )
#        price_csv.close()
#        print("... card price csv file created!")
#    return True

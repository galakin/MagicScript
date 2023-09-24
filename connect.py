import requests
import os
import pathlib
import pandas
import json
import argparse
import sys
import yaml

import src.priceCard as priceCard
import src.rwCsw as rwCsw
import src.connection as nwrk

import src.pdfManipulation as pdf
import src.exceptions as expt
import global_var

base_url = "https://api.cardtrader.com/api/v2"
game = "Magic"
# category = "Single Cards"

database_url = "https://api.scryfall.com"

# print("Fetching auth token...")
# print("auth token env: ", os.getenv("AUTH_TOKEN"))
if os.getenv("AUTH_TOKEN") != None:
    auth_token = os.getenv("AUTH_TOKEN")
#    print("...Auth token fetched from environment variables")

else:
    raise expt.InternalException("Unable to find auth token!")

headers = {"Authorization": auth_token}


def fetch_local_card_data():
    home_dir = os.getenv("HOME")
    if home_dir == None:
        raise expt.InternalException(
            "Unable to find environment variable named HOME\nplease check if you have defined it"
        )

    price_csw = pathlib.Path(global_var.custom_dir + "/price.csv")
    file_path = pathlib.Path(home_dir + "/card.csv")
    if file_path.is_file():
        print("Card file found!")
    else:
        raise expt.InternalException(
            "Unable to fin the card file a the default location!"
        )
    if price_csw.is_file():
        print("... card price csv file found!")
    else:
        price_csw = open(global_var.custom_dir + "/price.csv", "x")
        price_csw.writelines(["name,exp,min_price,max_price,mean_price\n"])
        price_csw.close()
        print("... card price csv file created!")
    return True


# TODO: rename module
def preliminary_action():
    home_dir = os.getenv("HOME")
    if home_dir == None:
        raise expt.InternalException(
            "Unable to find environment variable named HOME\nplease check if you have defined it"
        )

    else:
        if global_var.custom_dir == "":
            print("...Fetching files dir")
            with open(home_dir + "/.config/magicscript/config.yaml", "r") as stream:
                try:
                    config = yaml.safe_load(stream)
                    global_var.custom_dir = config["custom_dir"]
                    global_var.custom_output = config["custom_output"]
                    global_var.custom_name = config["custom_name"]
                    print(global_var.custom_dir)
                except yaml.YAMLError as e:
                    print(e)
    found_game = False
    if fetch_local_card_data():
        response = requests.get(base_url + "/games", headers=headers)
        # print(response.json()['array'])
        for elem in response.json()["array"]:
            if elem["name"] == game:
                print("Selected game found!")
                found_game = True
        if found_game == False:
            raise expt.InternalException("Unable to find selected Game")
    return True


def main(render=True):
    nwrk.verify_connection(base_url, headers)
    home_dir = os.getenv("HOME")
    if preliminary_action():
        try:
            print("Fetching card info...")
            # TODO change card csv file
            csv_file = rwCsw.read_csv(home_dir + "/card.csv")
            for elem in range(len(csv_file["card"])):
                try:
                    nwrk.search_for_card(
                        csv_file["card"][elem], database_url, base_url, headers
                    )
                except expt.InvalidTagException as ex:
                    print(ex)

            pdf.generate_pdf_report(csv_file["card"], render=render)

        except expt.InternalException as ex:
            print(ex)
            exit()

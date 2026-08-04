import requests
import os
import pathlib
import pandas
import json
import argparse
import sys
import yaml
import sys
import hashlib

import src.priceCard as priceCard
import src.rwCsw as rwCsw
import src.rwmysql as rwsql
import src.connection as nwrk

import src.pdfManipulation as pdf
import src.exceptions as expt
import global_var
import mysql_connect
import src.log_msg as logMsg

BUF_SIZE = 65536  # hasing buffer size
md5 = hashlib.md5()
sha1 = hashlib.sha1()

base_url = "https://api.cardtrader.com/api/v2"
game = "Magic"
# category = "Single Cards"

database_url = "https://api.scryfall.com"

if os.getenv("AUTH_TOKEN") != None:
    auth_token = os.getenv("AUTH_TOKEN")

else:
    raise expt.InternalException("Unable to find auth token!")

headers = {"Authorization": auth_token}


def fetch_local_card_data():
    home_dir = os.getenv("HOME")
    if home_dir == None:
        raise expt.InternalException(
            "Unable to find environment variable named HOME\nplease check if you have defined it"
        )
        return False

    price_csv = pathlib.Path(global_var.custom_dir + "/price.csv")
    file_path = pathlib.Path(home_dir + "/card.csv")
    if file_path.is_file():
        logMsg.loggin_messages("Card file found!")
    else:
        raise expt.InternalException(
            "Unable to fin the card file a the default location!"
        )
        return False
    if price_csv.is_file():
        logMsg.loggin_messages("... card price csv file found!")
    else:
        price_csv = open(global_var.custom_dir + "/price.csv", "x")
        price_csv.writelines(
            [
                "name,exp,min_price,max_price,mean_price,foil_min_price,foil_max_price,foil_mean_price,signed_min_price,signed_max_price,signed_mean_price,altered_min_price,altered_max_price,altered_mean_price\n"
            ]
        )
        price_csv.close()
        logMsg.loggin_messages("... card price csv file created!")
    return True


# TODO: rename module
def preliminary_action():
    home_dir = os.getenv("HOME")
    if home_dir == None:
        raise expt.InternalException(
            'Unable to find environment variable named "HOME"\nplease check if you have defined it'
        )
        return False

    else:
        if global_var.custom_dir == "":
            logMsg.loggin_messages("...Fetching files dir")
            with open(home_dir + "/.config/magicscript/config.yaml", "r") as stream:
                try:
                    config = yaml.safe_load(stream)
                    global_var.custom_dir = config["custom_dir"]
                    global_var.custom_output = config["custom_output"]
                    global_var.custom_name = config["custom_name"]
                    global_var.storage_method = config["storage_method"]
                    global_var.general_index = config["general_index"]
                except yaml.YAMLError as e:
                    logMsg.loggin_messages(f"{e}")
    found_game = False

    # check for the csv storage method [archived]
    if global_var.storage_method == "csv":
        if fetch_local_card_data():
            response = requests.get(base_url + "/games", headers=headers)
            for elem in response.json()["array"]:
                if elem["name"] == game:
                    logMsg.loggin_messages("Selected game found!")
                    found_game = True
            if found_game == False:
                raise expt.InternalException("Unable to find selected Game")
                return False

    # check for the mysql storage method
    elif global_var.storage_method == "mysql":
        logMsg.loggin_messages("Using mysql db as backend")
        mysql_connect.fetch_local_card_data()
        response = requests.get(base_url + "/games", headers=headers)
        for elem in response.json()["array"]:
            if elem["name"] == game:
                logMsg.loggin_messages("Selected game found!")
                found_game = True
        if found_game == False:
            raise expt.InternalException("Unable to find selected Game")
            return False
    return True


def fetch_card_list():

    with open(f"{os.getenv('HOME')}/card.csv", "r") as f:
        data = f.read(BUF_SIZE)
        sha1.update(data.encode("utf-8"))

    print("SHA1: {0}".format(sha1.hexdigest()))
    if rwsql.verify_hash(format(sha1.hexdigest())):
        logMsg.loggin_messages("No need to update internal collection")
        return mysql_connect.return_cards_list()
    else:
        logMsg.loggin_messages("Found change on the internal collection...updating DB")
        mysql_connect.update_card_info()
        return mysql_connect.return_cards_list()


def main(render=True):
    nwrk.verify_connection(base_url, headers)
    result = preliminary_action()
    if result:
        logMsg.loggin_messages("finished prelim action")
        try:
            import mysql.connector

            cards_list = fetch_card_list()
            logMsg.loggin_messages("Fetching card info...")

            # TODO: check csv compleatness
            for elem in cards_list:
                try:
                    if elem[1] != None:
                        nwrk.search_for_card(
                            elem[0],
                            elem[1],
                            database_url,
                            base_url,
                            headers,
                        )
                    else:
                        nwrk.search_for_card(
                            elem[0],
                            None,
                            database_url,
                            base_url,
                            headers,
                        )
                except expt.InvalidTagException as ex:
                    print(ex)
            if render:
                pdf.generate_pdf_report(cards_list)

        except expt.InternalException as ex:
            print("unexpected error")
            print(ex)
            exit()

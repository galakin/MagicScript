import os
import pandas
from datetime import date
import csv
import requests

import src.exceptions as expt
import global_var
import src.rwCsw as rwCsv


def check_card_csv(csv_path):
    if csv_path == None or csv_path == "":
        raise expt.InternalException("Unable to determine card csv path")

    with open(csv_path, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        first_row = True
        for row in csvreader:
            if first_row != True:
                if len(row) < 2:
                    print("No expansion code found for " + str(row[0]))
                    expansion_code = search_first_expansion(row[0])
                    if expansion_code != "":
                        rwCsv.write_expansion_code(row[0], expansion_code)
                    else:
                        raise expt.InternalException(
                            "Unable to determine expansion for " + str(row[0])
                        )
            first_row = False

    csvfile.close()


def search_first_expansion(card_name):
    if card_name == None or card_name == "":
        raise expt.InternalException("Unable to determine card name")

    card_json = requests.get(
        global_var.database_url + "/cards/named?exact=" + card_name
    )
    if card_json.json()["set"] != "":
        return card_json.json()["set"]

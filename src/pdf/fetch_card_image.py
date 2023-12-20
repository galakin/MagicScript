import requests
import os
import pathlib
import pandas
import json

import src.exceptions as expt
import global_var as gvar

# database_url = "https://api.scryfall.com"


def fetch_card_image(card_name, card_set=None):
    if card_name == None or card_name == "":
        raise expt.InternalException("Unable to determine card name")

    print("...Retriving card image")
    if card_set == None:
        card_json = requests.get(gvar.database_url + "/cards/named?exact=" + card_name)

    # print("card statud code:" + str(card_json.status_code))
    if card_json.status_code == 200:
        card_url = card_json.json()["image_uris"]["normal"]
        response = requests.get(card_url)

        check_dir_images()
        with open(
            gvar.custom_dir + "images/card_tmp/" + card_name + "_image.jpg", "wb"
        ) as f:
            None
            f.write(response.content)
    else:
        if card_set == None:
            card_json = requests.get(
                gvar.database_url + "/cards/named?fuzzy=" + card_name
            )


def cleanup():
    print("...clean up image directory")
    # os.removedirs(gvar.custom_dir + "images/card_tmp/")


def check_dir_images():
    if os.path.exists(gvar.custom_dir + "images/card_tmp/"):
        return True
    else:
        os.mkdir(gvar.custom_dir + "images/card_tmp/")
        return False

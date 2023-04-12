import requests
import os
import pathlib
import pandas  # TODO: change import location
import json

import src.priceCard as priceCard
import src.rwCsw as rwCsw

base_url = "https://api.cardtrader.com/api/v2"
game = "Magic"
category = "Single Cards"

database_url = "https://api.scryfall.com"

print("Fetching auth token...")
# print("auth token env: ", os.getenv("AUTH_TOKEN"))
if os.getenv("AUTH_TOKEN") != None:
    auth_token = os.getenv("AUTH_TOKEN")
    print("...Auth token fetched from environment variables")

else:
    raise Exception("Unable to find auth token!")

headers = {"Authorization": auth_token}


def verify_connection():
    ##Fetch game info
    response = requests.get(base_url + "/info", headers=headers)
    if response.status_code == 200:
        print("...Connection Established!\n")
    else:
        raise Exception(
            "Unable to connet to CardTrader API server\nCheck if your API token is still valid!"
        )


def fetch_local_card_data():
    home_dir = os.getenv("HOME")
    if home_dir == None:
        raise Exception(
            "Unable to find environment variable named HOME\nplease check if you have defined it"
        )

    else:
        price_csw = pathlib.Path(home_dir + "/.priceCsv/price.csv")
        file_path = pathlib.Path(home_dir + "/card.csv")
        if file_path.is_file():
            print("Card file found!")
        else:
            raise Exception("Unable to fin the card file a the default location!")
        if price_csw.is_file():
            print("... card price csv file found!")
        else:
            price_csw = open(home_dir + "/.priceCsv/price.csv", "x")
            price_csw.writelines(["name,exp,min_price,max_price,mean_price\n"])
            price_csw.close()
            print("... card price csv file created!")
    return True


# TODO: rename module
def preliminary_action():
    found_game = False
    if fetch_local_card_data():
        response = requests.get(base_url + "/games", headers=headers)
        # print(response.json()['array'])
        for elem in response.json()["array"]:
            if elem["name"] == game:
                print("Selected game found!")
                found_game = True
        if found_game == False:
            raise Exception("Unable to find selected Game")
    return True


def search_for_card(name):
    blueprint_id = -1
    expansion_id = -1
    expansion_name = ""

    card_json = requests.get(database_url + "/cards/named?exact=" + name)
    if card_json.status_code != 200:
        exit()
    scryfall_id = card_json.json()["id"]
    card_expansion_code = card_json.json()["set"]
    expansion_code = requests.get(base_url + "/expansions", headers=headers)
    if expansion_code.status_code != 200:
        exit()

    print("...Retrived the list of expansions")
    for elem in expansion_code.json():
        if elem["code"] == card_expansion_code:
            if expansion_id > 0:
                exit()
            expansion_id = elem["id"]
            expansion_name = elem["code"]
            print("...Card code found!")

    # retrive card blueprint
    card_blueprint = requests.get(
        base_url + "/blueprints/export?expansion_id=" + str(expansion_id),
        headers=headers,
    )
    if card_blueprint.status_code != 200:
        raise Exception("unable to fetch expensions card")

    for elem in card_blueprint.json():
        if elem["name"] == name:
            if blueprint_id > 0:
                raise Exception("two product with the same name found")
            blueprint_id = elem["id"]

    selled_cards = requests.get(
        base_url + "/marketplace/products?blueprint_id=" + str(blueprint_id),
        headers=headers,
    )
    tst = list(selled_cards.json().keys())

    print("...feteching prices info")
    card_price = priceCard.get_prices(selled_cards.json(), tst[0])
    # print(card_price)
    rwCsw.write_to_csv(name, expansion_name, card_price)


verify_connection()
if preliminary_action():
    print("Fetching card info...")
    csv_file = rwCsw.read_csv()
    for elem in range(len(csv_file["card"])):
        search_for_card(csv_file["card"][elem])

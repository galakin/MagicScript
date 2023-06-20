import requests
import os
import pathlib
import pandas  # TODO: change import location
import json

import src.priceCard as priceCard
import src.rwCsw as rwCsw
import src.exceptions as expt
import src.stocks as stocks


def verify_connection(base_url, headers):
    ##Fetch game info
    response = requests.get(base_url + "/info", headers=headers)
    if response.status_code == 200:
        print("...Connection Established!\n")
    else:
        raise expt.InternalException(
            "Unable to connet to CardTrader API server\nCheck if your API token is still valid!"
        )


def search_for_card(name, database_url, base_url, headers):
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
        raise expt.InternalException("unable to fetch expensions card")

    for elem in card_blueprint.json():
        if elem["name"] == name:
            if blueprint_id > 0:
                raise expt.InternalException("two product with the same name found")
            blueprint_id = elem["id"]

    selled_cards = requests.get(
        base_url + "/marketplace/products?blueprint_id=" + str(blueprint_id),
        headers=headers,
    )

    tst = list(selled_cards.json().keys())

    print("...fetching prices info")
    if tst[0] != "error":
        card_price = priceCard.get_prices(selled_cards.json(), tst[0])
        stocks.finds_stocks(selled_cards.json(), blueprint_id)

        rwCsw.write_to_csv(name, expansion_name, card_price)
    else:
        raise expt.InvalidTagException(
            "Unable to find item with elem_id=", blueprint_id
        )

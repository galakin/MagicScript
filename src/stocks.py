import fpdf
import numpy
import pandas
import os
from datetime import date
from matplotlib import rcParams
import matplotlib.pyplot as plt

import src.rwCsw as rwCsw
import src.exceptions as expt


def finds_stocks(selled_cards, blueprint_id):
    if len(selled_cards) == 0:
        raise expt.InternalException(
            "Unable to fetch seller list for item with tag: " + str(selled_cards)
        )
    if blueprint_id == None:
        raise expt.InternalException(
            'Item tag: "' + str(blueprint_id) + "\" isn't specified correctly"
        )
    name = selled_cards[str(blueprint_id)][0]["name_en"]
    stock_no = len(selled_cards[str(blueprint_id)])
    foil_stock = 0
    alter_stock = 0
    signed_stock = 0
    for elem in selled_cards[str(blueprint_id)]:
        if elem["properties_hash"]["mtg_foil"] == True:
            foil_stock += 1
        if elem["properties_hash"]["signed"] == True:
            signed_stock += 1
        if elem["properties_hash"]["altered"] == True:
            alter_stock += 1

    rwCsw.write_stock_csv(
        name,
        {
            "stocks": stock_no,
            "foil": foil_stock,
            "signed": signed_stock,
            "altered": alter_stock,
        },
    )

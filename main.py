import requests
import os
import pathlib
import pandas
import json

import src.priceCard as priceCard
import src.rwCsw as rwCsw
import src.connection as nwrk
import src.pdfManipulation as pdf
import src.exceptions as expt

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


if __name__ == "__main__":
    nwrk.verify_connection(base_url, headers)
    if preliminary_action():
        try:
            print("Fetching card info...")
            csv_file = rwCsw.read_csv("/card.csv")
            for elem in range(len(csv_file["card"])):
                try:
                    nwrk.search_for_card(
                        csv_file["card"][elem], database_url, base_url, headers
                    )
                except expt.InvalidTagException as ex:
                    print(ex)

            pdf.generate_pdf_report(csv_file["card"])
        except Exception as ex:
            print(ex)
            exit()

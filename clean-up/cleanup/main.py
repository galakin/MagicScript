import json
import sys
import yaml
import os
from datetime import datetime
import calendar
import mysql.connector

import src.exceptions as expt
import global_var
import mysql_connect
import src.log_msg as logMsg
import src.cleanup.clean_price as cleanPrice
import src.cleanup.retrieve_db_credential as retrieveCredentials

"""
Start the Database cleanup process that remove entry older than 3 month
"""


def return_cards_list(username, password):
    database = mysql.connector.connect(
        host="localhost", user=username, password=password
    )
    try:
        mycursor = database.cursor()
        mycursor.execute("USE cards_database;")
        mycursor.execute("SELECT * FROM card_info;")
        return_list = []
        for elem in mycursor:
            return_list.append(elem)
        return return_list
    except Exception as e:
        print(e)
        exit(-1)


def main():
    # TODO: extract username and password from env
    logMsg.loggin_messages("Starting the Database cleanup process")
    creds = retrieveCredentials.retrieve_credentials("", "")

    card_list = return_cards_list(creds[0], creds[1])

    try:
        for elem in card_list:
            print(f"{elem[0]} - {elem[1]}")
            remove_year_old_entry(elem[0], elem[1])
    except Exception as e:
        print(e)
        return -1

    #    logMsg.loggin_messages("Connecting to database...")
    #    database = mysql.connector.connect(
    #        host="localhost", user=username, password=password
    #    )
    #
    #    mycursor = database.cursor()
    #    mycursor.execute("USE cards_database;")
    #
    #    month_epoch_delta = 0

    return 0


"""
Remove entry older than 1 year and merge them in one entry for every 3 month
card_name: name of the single card that it's used for search entry on the main database
card_sat: the Magic set of the card, used to connect to the correct DB entry
"""


def remove_year_old_entry(card_name, card_set):
    last_year = datetime(
        datetime.now().year - 1, datetime.now().month, datetime.now().day
    )
    last_year_epoch = calendar.timegm(last_year.timetuple())
    # print(f"{last_year} -- {last_year_epoch}")

    table_name = (
        card_name.lower().replace(" ", "_", card_name.count(""))
        + "_"
        + card_set
        + "_price"
    )
    # print(table_name)
    cleanPrice.clean_price(table_name, last_year_epoch, "YEAR")
    return 0

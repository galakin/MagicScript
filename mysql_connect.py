import requests
import os
import pathlib
import pandas
import json
import argparse
import sys
import yaml
import mysql.connector

import src.priceCard as priceCard
import src.rwCsw as rwCsw
import src.connection as nwrk

import src.pdfManipulation as pdf
import src.exceptions as expt
import src.log_msg as logMsg
import global_var


def fetch_local_card_data():
    database = mysql.connector.connect(
        host="localhost", user="root", password="cul5ai2xnsgs"
    )

    mycursor = database.cursor()
    mycursor.execute("SHOW DATABASES;")

    find_db = False
    for elem in mycursor:
        if elem[0] == "cards_database":
            find_db = True
    if find_db:
        logMsg.loggin_messages("...cards db found")
        mycursor.execute("USE cards_database;")
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS `card_info`(card varchar(255), expansion varchar(255), card_condition varchar(255))"
        )
        mycursor.execute("SELECT * FROM card_info")

        rowcount = 0
        for elem in mycursor:
            rowcount += 1

        if rowcount == 0:
            populate_database()
        else:
            check_cards_data_update()

    else:
        logMsg.loggin_messages("...Unable to find cards db")
        mycursor.execute("CREATE DATABASE cards_database")
        database.commit()
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS `card_info`(card varchar(255), expansion varchar(255), card_condition varchar(255))"
        )
        database.commit()
        populate_database()
    return True


# populate the card_info database if it's find empty
def populate_database():
    import csv

    database = mysql.connector.connect(
        host="localhost", user="root", password="cul5ai2xnsgs"
    )

    mycursor = database.cursor()

    home_dir = os.getenv("HOME")
    if home_dir == None:
        raise expt.InternalException(
            "Unable to find environment variable named HOME\nplease check if you have defined it"
        )
        return False

    file_path = pathlib.Path(home_dir + "/card.csv")
    if file_path.is_file():
        with open(file_path, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            first_row = True
            for row in csvreader:
                if first_row == True:
                    first_row = False
                else:
                    mycursor.execute("USE cards_database;")
                    if len(row) < 3:
                        mycursor.execute(
                            "INSERT INTO card_info (card, expansion, card_condition) VALUES ('"
                            + row[0]
                            + "', '"
                            + row[1]
                            + "', 'nodata');"
                        )
                    else:
                        mycursor.execute(
                            "INSERT INTO card_info ('"
                            + row[0]
                            + "', '"
                            + row[1]
                            + "', '"
                            + row[2]
                            + "');"
                        )
                    database.commit()

    else:
        raise expt.InternalException(
            "Unable to fin the card file a the default location!"
        )
        return False
    return True


def check_cards_data_update():
    return True
    # TODO: write body


def return_cards_list():
    database = mysql.connector.connect(
        host="localhost", user="root", password="cul5ai2xnsgs"
    )

    mycursor = database.cursor()
    mycursor.execute("USE cards_database;")
    mycursor.execute("SELECT * FROM card_info;")
    return_list = []
    for elem in mycursor:
        return_list.append(elem)
    return return_list

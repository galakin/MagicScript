import os
import pandas
import calendar
from datetime import date
import mysql.connector

import src.exceptions as expt
import src.log_msg as logMsg


def write_stock_csv(name, stocks, expansion_name):
    database = mysql.connector.connect(
        host="localhost", user="root", password="cul5ai2xnsgs"
    )

    mycursor = database.cursor()
    mycursor.execute("USE cards_database;")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS `"
        + name.lower().replace(" ", "_", name.count(""))
        + "_"
        + str(expansion_name)
        + "_stock`(stocks int, foil int, signed int, altered int, stock_date int )"
    )
    mycursor.execute(
        "SELECT stock_date FROM `"
        + name.lower().replace(" ", "_", name.count(""))
        + "_"
        + str(expansion_name)
        + "_stock`"
    )
    find_date = True
    # TODO: order date and select only the newest
    for elem in mycursor:
        if elem[0] == calendar.timegm(date.today().timetuple()):
            find_date = False
    if find_date:
        mycursor.execute(
            "INSERT INTO "
            + name.lower().replace(" ", "_", name.count(""))
            + "_"
            + str(expansion_name)
            + "_stock ("
            + "stocks, foil, signed, altered, stock_date) VALUES ("
            + str(stocks["stocks"])
            + ", "
            + str(stocks["foil"])
            + ", "
            + str(stocks["signed"])
            + ", "
            + str(stocks["altered"])
            + ", "
            + str(calendar.timegm(date.today().timetuple()))
            + ");"
        )
        database.commit()
    return True


def write_to_csv(name, expansion_code, prices):
    logMsg.loggin_messages("write data to csv")
    database = mysql.connector.connect(
        host="localhost", user="root", password="cul5ai2xnsgs"
    )

    mycursor = database.cursor()
    mycursor.execute("USE cards_database;")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS `"
        + name.lower().replace(" ", "_", name.count(""))
        + "_"
        + str(expansion_code)
        + "_price`"
        + "(min_price float, max_price float, mean_price float, "
        + "foil_min_price float, foil_max_price float, foil_mean_price float,"
        + "signed_min_price float, signed_max_price float, signed_mean_price float,"
        + "altered_min_price float, altered_max_price float, altered_mean_price float, "
        + "price_date int )"
    )

    mycursor.execute(
        "SELECT price_date FROM `"
        + name.lower().replace(" ", "_", name.count(""))
        + "_"
        + str(expansion_code)
        + "_price`;"
    )
    find_date = True
    # TODO: order date and select only the newest
    for elem in mycursor:
        if elem[0] == calendar.timegm(date.today().timetuple()):
            find_date = False

    if find_date:
        mycursor.execute(
            "INSERT INTO "
            + name.lower().replace(" ", "_", name.count(""))
            + "_"
            + str(expansion_code)
            + "_price "
            + "(min_price, max_price, mean_price, "
            + "foil_min_price, foil_max_price, foil_mean_price, "
            + "signed_min_price, signed_max_price, signed_mean_price, "
            + "altered_min_price, altered_max_price, altered_mean_price, "
            + "price_date) VALUES ("
            + str(prices["min_price"])
            + ", "
            + str(prices["max_price"])
            + ", "
            + str(prices["mean_price"])
            + ", "
            + str(prices["foil_min_price"])
            + ", "
            + str(prices["foil_max_price"])
            + ", "
            + str(prices["foil_mean_price"])
            + ", "
            + str(prices["signed_min_price"])
            + ", "
            + str(prices["signed_max_price"])
            + ", "
            + str(prices["signed_mean_price"])
            + ", "
            + str(prices["altered_min_price"])
            + ", "
            + str(prices["altered_max_price"])
            + ", "
            + str(prices["altered_mean_price"])
            + ", "
            + str(calendar.timegm(date.today().timetuple()))
            + ");"
        )
        database.commit()


def verify_hash(hash_code):
    return True

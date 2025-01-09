import pandas
import datetime
import calendar

import src.exceptions as expt
import src.rwCsw as rwCsw

""" return the price in the latest month time frame
    card_info: complete list of card information with card name and expansion
    list_elem: list of card type that need to be rendered/filtered
"""


def render_prices_month(card_info, list_elem):
    import mysql.connector

    print("...render latest month prices")

    database = mysql.connector.connect(
        host="localhost", user="root", password="cul5ai2xnsgs"
    )

    mycursor = database.cursor()
    mycursor.execute("USE cards_database;")

    select_fields = ""
    for elem in range(len(list_elem)):
        if elem < len(list_elem) - 1:
            select_fields = select_fields + str(list_elem[elem]) + ", "
        else:
            select_fields = select_fields + str(list_elem[elem])

    tod = datetime.datetime.now().date()
    delta = datetime.timedelta(days=30)
    time_range = tod - delta

    lower_epoch = calendar.timegm(
        datetime.datetime(
            time_range.year, time_range.month, time_range.day, 0, 0, 0
        ).timetuple()
    )
    mycursor.execute(
        "SELECT "
        + select_fields
        + " FROM `"
        + card_info[0].lower().replace(" ", "_", card_info[0].count(""))
        + "_"
        + str(card_info[1])
        + "_price` WHERE price_date > "
        + str(lower_epoch)
    )

    rendered_date_price = {}

    # generate the empty elem in for every item in list_elem on the map rendered_date_price
    for elem in list_elem:
        rendered_date_price[elem] = []

    # populate the rendered_date_price
    for elem in mycursor:
        for field_index in range(len(list_elem)):
            rendered_date_price[list_elem[field_index]].append(elem[field_index])

    # print(rendered_date_price)
    return rendered_date_price


""" render the stock month info """
# TODO: implemet the field list
def render_stock_month(card_info, list_elem):
    import mysql.connector

    print("...render latest month prices")

    database = mysql.connector.connect(
        host="localhost", user="root", password="cul5ai2xnsgs"
    )

    mycursor = database.cursor()
    mycursor.execute("USE cards_database;")

    print("...render latest month stock for " + str(card_info[0]))

    tod = datetime.datetime.now().date()
    delta = datetime.timedelta(days=30)
    time_range = tod - delta

    lower_epoch = calendar.timegm(
        datetime.datetime(
            time_range.year, time_range.month, time_range.day, 0, 0, 0
        ).timetuple()
    )

    mycursor.execute(
        "SELECT * FROM `"
        + card_info[0].lower().replace(" ", "_", card_info[0].count(""))
        + "_"
        + str(card_info[1])
        + "_stock` WHERE stock_date > "
        + str(lower_epoch)
    )

    rendered_stock_price = {}
    for elem in list_elem:
        rendered_stock_price[elem] = []

    for elem in mycursor:
        for field_index in range(len(list_elem)):
            rendered_stock_price[list_elem[field_index]].append(elem[field_index])

    return rendered_stock_price

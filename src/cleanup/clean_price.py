import json
import sys
import yaml
import os
from datetime import datetime
import calendar
import mysql.connector

from datetime import datetime
from dateutil.relativedelta import relativedelta

import src.exceptions as expt
import global_var
import mysql_connect
import src.log_msg as logMsg
import src.cleanup.retrieve_db_credential as retrieveCredentials


"""Cleanup the price table for the selected card"""


def clean_price(card_table, time_epoch, paramether):
    creds = retrieveCredentials.retrieve_credentials("", "")
    print(f"{card_table} -- {time_epoch} -- {paramether}")
    match paramether:
        # Compress the database on a yearly range
        case "YEAR":
            database = mysql.connector.connect(
                host="localhost", user=creds[0], password=creds[1]
            )
            try:
                mycursor = database.cursor()
                mycursor.execute(f"USE cards_database;")
                mycursor.execute(
                    f"SELECT * FROM {card_table} WHERE price_date < {time_epoch};"
                )

                results = mycursor.fetchall()
                sorted_result = sorted(results, key=lambda x: x[12])
                bottom_end_epoch = sorted_result[0][12]

                delta_time = 1000
                while (time_epoch - delta_time) > bottom_end_epoch:
                    time_epoch = time_epoch - delta_time
                    None
                print(bottom_end_epoch)
                # for elem in sorted_result:
                #    print(elem[12])
                # count = mycursor.rowcount
                # print(f"Total rows returned: {count}")
                # print(mycursVor)
            except Exception as e:
                print(e)
                exit(-1)
        case "MONTH":
            None
    return 0

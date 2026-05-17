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


"""Cleanup the price table for the selected card
    card_table: the table associated with the selected card
    time_epoch: the starting time epoch
    paramethers: if the cleanup need to be done on a yearly, monthly or weekly base
"""


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

                init_mont = 0
                target_date = datetime(
                    datetime.now().year - 1, datetime.now().month, datetime.now().day
                )
                delta_time = target_date - relativedelta(months=init_mont)
                print(delta_time)

                while (target_date.timestamp() - bottom_end_epoch) > 0:
                    init_mont += 3
                    mycursor.execute(
                        f"SELECT * FROM {card_table} WHERE price_date < {target_date.timestamp()} AND price_date >= {(target_date - relativedelta(months=init_mont)).timestamp()};"
                    )
                    results = mycursor.fetchall()
                    # print(results)
                    # check if there are more than one entry for the yearly time frame
                    if not check_compacted_data(results):
                        compact_result = compact_data(results)
                        print(len(compact_result))
                    # mycursor.execute(f"DELETE FROM {card_table} (WHERE price_date IN (0));")
                    #                    mycursor.execute(
                    #                        f"INSERT INTO {card_table} (
                    #                            min_prices, max_prices, mean_prices, foil_min_prices, foil_max_prices, foil_mean_prices, signed_min_prices, signed_max_prices, signed_mean_prices,
                    #                            alterd_min_prices, altered_max_prices, altered_mean_prices, price_date
                    #                        )
                    #                        VALUES (
                    #                            {compact_data['0']}, {compact_data['1']}, {compact_data['2']}, {compact_data['3']}, {compact_data['4']}, {compact_data['5']},
                    #                            {compact_data['6']}, {compact_data['7']}, {compact_data['8']}, {compact_data['9']}, {compact_data['10']}, {compact_data['11']},
                    #                            {compact_data['12']}
                    #                        );"
                    #                    )
                    # database.commit()
                    target_date = target_date - relativedelta(months=init_mont)
                print(bottom_end_epoch)
            except Exception as e:
                print(e)
                exit(-1)
        case "MONTH":
            None
    return 0


# https://github.com/OWNER/REPOSITORY/actions/workflows/WORKFLOW-FILE/badge.svg


def compact_data(extracted_data):
    compact_result = {}
    for single_entry in extracted_data:
        for index in range(len(single_entry)):
            if str(index) not in compact_result:
                compact_result[str(index)] = single_entry[index]

            else:
                compact_result[str(index)] += single_entry[index]
    for key in compact_result:
        compact_result[key] = compact_result[key] / len(extracted_data)

    return compact_result


def check_compacted_data(extracted_data):
    if len(extracted_data) > 1:
        None
        return False
    else:
        return True

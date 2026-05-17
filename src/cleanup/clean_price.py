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

# timefra for GEN-MAR APR-JUN JUL-SET OCT-DEC
# TIMEFRAME = {(1, 3), (4, 6), (7, 9), (10, 12)}


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

                # fetch all data over the past yeat
                results = mycursor.fetchall()

                sorted_result = sorted(results, key=lambda x: x[12])
                bottom_end_epoch = sorted_result[0][12]
                init_mont = 0

                # get all the data from 1 year ago to the start of the fetched data
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
                    if len(results) > 1:
                        compact_result = compact_data(results)
                        print(compact_result)
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

    first_month = 0  # check if it's the start of a new 3 month windows
    month_upper_limit = 0  # the month where the next 3 month windows trigger
    map_index = 0  # index for the freshly created map that store compacted data
    temp_compact_result = {}
    for single_entry in extracted_data:
        # get the db entry date timestamp
        data_now = datetime.fromtimestamp(single_entry[len(single_entry) - 1])
        if first_month == 0:
            first_month = data_now.month
            month_upper_limit = get_month_upper_limit(data_now.month)
            # print(first_month)

        if data_now.month > month_upper_limit:
            compact_result[str(map_index)] = temp_compact_result
            temp_compact_result = {}
            first_month = data_now.month
            month_upper_limit = get_month_upper_limit(data_now.month)
            map_index += 1

        # print(data_now.month)
        # print(single_entry[len(single_entry) - 1])

        for index in range(len(single_entry)):
            if str(index) not in compact_result:
                temp_compact_result[str(index)] = single_entry[index]

            else:
                temp_compact_result[str(index)] += single_entry[index]
    # for key in compact_result:
    #    compact_result[key] = compact_result[key] / len(extracted_data)

    return compact_result


"""
return the month upper limit for the current month following the schema
specified in the project issue
current_month: the current month for the analyzed entry
"""


def get_month_upper_limit(current_month):
    if current_month <= 3:
        return 3
    elif current_month > 3 and current_month <= 6:
        return 6
    elif current_month > 6 and current_month <= 9:
        return 9
    else:  # current_month > 9
        return 12

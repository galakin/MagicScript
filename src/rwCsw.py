import os
import pandas
from datetime import date


def write_main_dir():
    home_dir = os.getenv("HOME")
    if not os.path.isdir(home_dir + "/.priceCsv"):
        print('... Creating hidden directory at path "' + str(home_dir + "/.priceCsv"))
        os.mkdir(home_dir + "/.priceCsv")


def write_to_csv(name, exp, prices):
    write_main_dir()
    row_no = search_row(name, "name", "price.csv")
    home_dir = os.getenv("HOME")
    price_csv = open(home_dir + "/.priceCsv/price.csv", "a")
    if row_no != -1:
        pandas_csv = pandas.read_csv(home_dir + "/.priceCsv/price.csv")
        pandas_csv.at[row_no, "min_price"] = prices["min_price"]
        pandas_csv.at[row_no, "max_price"] = prices["max_price"]
        pandas_csv.at[row_no, "mean_price"] = prices["mean_price"]
        pandas_csv.to_csv(home_dir + "/.priceCsv/price.csv", index=False)

    else:
        price_csv.writelines(
            [
                str(name)
                + ","
                + str(exp)
                + ","
                + str(prices["min_price"])
                + ","
                + str(prices["max_price"])
                + ","
                + str(prices["mean_price"])
                + "\n"
            ]
        )
    price_csv.close()
    write_card_price_csv(name, prices)


def write_card_price_csv(name, prices):
    home_dir = os.getenv("HOME")
    if not os.path.isfile(
        home_dir
        + "/.priceCsv/"
        + name.lower().replace(" ", "/", name.count(""))
        + "_price.csv"
    ):
        price_csv = open(
            home_dir
            + "/.priceCsv/"
            + name.lower().replace(" ", "/", name.count(""))
            + "_price.csv",
            "a",
        )
        price_csv.writelines(["date,min_price,max_price,mean_price\n"])
        price_csv.close()
    if (
        search_row(
            date.today(),
            "date",
            name.lower().replace(" ", "/", name.count("")) + "_price.csv",
        )
        == -1
    ):
        price_csv = open(
            home_dir
            + "/.priceCsv/"
            + name.lower().replace(" ", "/", name.count(""))
            + "_price.csv",
            "a",
        )
        price_csv.writelines(
            [
                str(date.today())
                + ","
                + str(prices["min_price"])
                + ","
                + str(prices["max_price"])
                + ","
                + str(prices["mean_price"])
                + "\n"
            ]
        )
        price_csv.close()


def read_csv():
    home_dir = os.getenv("HOME")
    if home_dir != None:
        csv_file = pandas.read_csv("/home/jacopopela/card.csv")
    else:
        csv_file = pandas.read_csv(str(home_dir) + "card.csv")
    return csv_file


def search_row(name, field_name, file_name):
    home_dir = os.getenv("HOME")
    if home_dir == None:
        exit(-1)
    else:
        csv_file = pandas.read_csv(str(home_dir) + "/.priceCsv/" + file_name)
    index = 0
    for elem in range(len(csv_file[field_name])):
        if str(csv_file[field_name][elem]) == str(name):
            return index
        index += 1
    # for elem in rage(
    return -1

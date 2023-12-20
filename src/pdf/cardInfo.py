import fpdf
import numpy
import pandas
import os
from datetime import date
import datetime
from matplotlib import rcParams
import matplotlib.pyplot as plt

import src.rwCsw as rwCsw
import src.stocks as stocks
import src.dateRender as drender
import global_var
import src.pdf.fetch_card_image as fci


def generate_info(name, pdf):
    print("...Rendering " + str(name) + " info page")

    # retrive info for card stock
    filter_stock_csw = drender.render_stock_month(
        global_var.custom_dir
        + str(name).lower().replace(" ", "/", name.count(""))
        + "_stock.csv"
    )
    start_stock = filter_stock_csw.iloc[[0]]["stock"].values[0]

    end_stock = filter_stock_csw.iloc[[len(filter_stock_csw) - 1]]["stock"].values[0]
    # print("start stock: "+str(start_stock)+" end stock: "+str(end_stock))

    #          date  stock  foil  signed  altered
    start_foil, end_foil = (
        filter_stock_csw.iloc[[0]]["foil"].values[0],
        filter_stock_csw.iloc[[len(filter_stock_csw) - 1]]["foil"].values[0],
    )
    start_signed, end_signed = (
        filter_stock_csw.iloc[[0]]["signed"].values[0],
        filter_stock_csw.iloc[[len(filter_stock_csw) - 1]]["signed"].values[0],
    )

    # retrive info for card prices
    filter_price_csw = drender.render_prices_month(
        global_var.custom_dir
        + str(name).lower().replace(" ", "/", name.count(""))
        + "_price.csv",
        ["date", "min_price", "max_price", "mean_price"],
    )

    start_min, start_max, start_mean = (
        filter_price_csw.iloc[[0]]["min_price"].values[0],
        filter_price_csw.iloc[[0]]["max_price"].values[0],
        filter_price_csw.iloc[[0]]["mean_price"].values[0],
    )
    end_min, end_max, end_mean = (
        filter_price_csw.iloc[[len(filter_price_csw) - 1]]["min_price"].values[0],
        filter_price_csw.iloc[[len(filter_price_csw) - 1]]["max_price"].values[0],
        filter_price_csw.iloc[[len(filter_price_csw) - 1]]["mean_price"].values[0],
    )

    result = {
        "delta_stock": end_stock - start_stock,
        "percentage_stock": end_stock * 100 / start_stock,
        "delta_foil": end_foil - start_foil,
        "percentage_foil": end_foil * 100 / start_foil,
        "delta_signed": end_signed - start_signed,
        "percentage_signed": end_signed * 100 / start_signed,
    }

    # retrive card image
    fci.fetch_card_image(name)

    pdf.add_page()
    pdf.cell(60, 10, "Info for " + str(name), 0, 1)
    pdf.cell(
        60,
        10,
        "Prices and stocks fetched between: \t\t"
        + str(datetime.datetime.now().date() - datetime.timedelta(days=30))
        + " and "
        + str(date.today()),
        0,
        1,
    )
    pdf.cell(
        60,
        30,
        "Stock info",
        0,
        1,
    )
    pdf.cell(
        60,
        10,
        "Starting stock: \t\t" + str(start_stock) + " \t end stock: " + str(end_stock),
        0,
        1,
    )
    pdf.cell(
        60, 0, "Delta of stock: \t\t" + str(result["delta_stock"]) + " units", 0, 1
    )
    pdf.cell(
        60,
        10,
        "Percentage grow of stock: \t\t"
        + str(round(result["percentage_stock"] - 100, 2))
        + "%",
        0,
        1,
    )

    pdf.cell(
        60,
        10,
        "Starting foil stock: \t\t"
        + str(start_foil)
        + " \t end stock: "
        + str(end_foil),
        0,
        1,
    )
    pdf.cell(
        60, 0, "Delta of foil cards: \t\t" + str(result["delta_foil"]) + " units", 0, 1
    )
    result["percentage_foil"] = round(result["percentage_foil"], 2) - 100
    pdf.cell(
        60,
        10,
        "Percentage grow of foil cards: \t"
        + str(round(result["percentage_foil"], 2))
        + "%",
        0,
        1,
    )

    pdf.cell(
        60,
        10,
        "Starting of signed stock: \t\t"
        + str(start_signed)
        + " \t end stock: "
        + str(end_signed),
        0,
        1,
    )
    pdf.cell(
        60,
        0,
        "Delta of signed cards: \t\t" + str(result["delta_signed"]) + " units",
        0,
        1,
    )
    if result["delta_signed"] < 0:
        result["percentage_signed"] = round(result["percentage_signed"], 2) - 100
    elif result["delta_signed"] >= 0:
        result["percentage_signed"] = 100 - round(result["percentage_signed"], 2)
    if numpy.isnan(result["percentage_signed"]):
        result["percentage_signed"] = 0
    pdf.cell(
        60,
        10,
        "Percentage grow of signed cards: \t\t"
        + str(round(result["percentage_signed"], 2))
        + "%",
        0,
        1,
    )

    # Prices information
    pdf.cell(
        60,
        30,
        "Prices info",
        0,
        1,
    )
    pdf.cell(
        60,
        10,
        "Starting of min price: \t\t"
        + str(start_min)
        + " \t end of min price: "
        + str(end_min),
        0,
        1,
    )
    pdf.cell(
        60,
        0,
        "Delta of min prices: \t\t" + str(round(end_min - start_min, 2)),
        0,
        1,
    )
    percentage = 0
    if end_min - start_min < 0:
        percentage = round(end_min * 100 / start_min, 2) - 100
    elif end_min - start_min >= 0:
        percentage = round(end_min * 100 / start_min, 2) - 100
    pdf.cell(
        60,
        10,
        "Percentage grow of min price: \t\t" + str(round(percentage, 2)) + "%",
        0,
        1,
    )

    pdf.cell(
        60,
        10,
        "Starting of max price: \t\t"
        + str(start_max)
        + " \t end of max price: "
        + str(end_max),
        0,
        1,
    )
    pdf.cell(
        60,
        0,
        "Delta of max prices: \t\t" + str(round(end_max - start_max, 2)),
        0,
        1,
    )
    if end_max - start_max < 0:
        percentage = round(end_max * 100 / start_max, 2) - 100
    elif end_max - start_max >= 0:
        percentage = round(end_max * 100 / start_max, 2) - 100
    pdf.cell(
        60,
        10,
        "Percentage grow of max price: \t\t" + str(percentage) + "%",
        0,
        1,
    )

    pdf.cell(
        60,
        10,
        "Starting of mean price: \t\t"
        + str(round(start_mean, 2))
        + " \t end of mean price: "
        + str(round(end_mean, 2)),
        0,
        1,
    )
    pdf.cell(
        60,
        0,
        "Delta of mean prices: \t\t" + str(round(end_mean - start_mean, 2)),
        0,
        1,
    )
    if (end_mean - start_mean) < 0:
        percentage = round((end_mean * 100 / start_mean) - 100, 2)
    elif (end_mean - start_mean) >= 0:
        percentage = round((end_mean * 100 / start_mean) - 100, 2)
    pdf.cell(
        60,
        10,
        "Percentage grow of mean price: \t\t" + str(percentage) + "%",
        0,
        1,
    )

    pdf.image(
        global_var.custom_dir + "images/card_tmp/" + name + "_image.jpg",
        x=130,
        y=40,
        w=0,
        h=90,
    )

    fci.cleanup()

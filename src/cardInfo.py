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


def generate_info(name, pdf):
    print("...Rendering " + str(name) + " info page")

    filter_price_csw = drender.render_stock_month(
        "/.priceCsv/"
        + str(name).lower().replace(" ", "/", name.count(""))
        + "_stock.csv"
    )
    start_stock = filter_price_csw.iloc[[0]]["stock"].values[0]
    # print(filter_price_csw)

    end_stock = filter_price_csw.iloc[[len(filter_price_csw) - 1]]["stock"].values[0]
    # print("start stock: "+str(start_stock)+" end stock: "+str(end_stock))

    #          date  stock  foil  signed  altered
    start_foil, end_foil = (
        filter_price_csw.iloc[[0]]["foil"].values[0],
        filter_price_csw.iloc[[len(filter_price_csw) - 1]]["foil"].values[0],
    )
    start_signed, end_signed = (
        filter_price_csw.iloc[[0]]["signed"].values[0],
        filter_price_csw.iloc[[len(filter_price_csw) - 1]]["signed"].values[0],
    )
    result = {
        "delta_stock": end_stock - start_stock,
        "percentage_stock": end_stock * 100 / start_stock,
        "delta_foil": end_foil - start_foil,
        "percentage_foil": end_foil * 100 / start_foil,
        "delta_signed": end_signed - start_signed,
        "percentage_signed": end_signed * 100 / start_signed,
    }

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
        + str(round(result["percentage_stock"], 2))
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
    # pdf_page = fpdf.FPDF
    # print("stock's delta: "+str(delta_stock))
    # print("percentage stock's delta: "+str(percentage_stock))

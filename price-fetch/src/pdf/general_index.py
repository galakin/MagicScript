# import fpdf
# import numpy
# import pandas
# import os
# from datetime import date
# import datetime
# from operator import add
# import matplotlib.pyplot as plt
#
# import src.rwmysql as rwm
# import src.stocks as stocks
# import src.dateRender as drender
# import src.exceptions as expt
# import global_var
#
# """
# Create the general index page, this is the first page of the document with data collected for all the card in the collection
# pdf: the pdf file that is generated
# csv_file: the list that contain all the information for the cards collection
# """
#
#
# def general_index(pdf, csv_file):
#    price_page(pdf, csv_file)
#    stock_page(pdf, csv_file)
#
#
# def price_page(pdf, csv_file):
#    # print(csv_file)
#
#    collection = [
#        {0: 0, 1: "Min", 2: []},
#        {0: 0, 1: "Max", 2: []},
#        {0: 0, 1: "Mean", 2: []},
#    ]
#    for elem in csv_file:
#        price_elem = drender.render_prices_month(
#            elem, ["price_date", "min_price", "max_price", "mean_price"]
#        )
#
#        if len(collection[0][2]) == 0:
#            collection[0][2] = price_elem["min_price"]
#        else:
#            collection[0][2] = list(map(add, price_elem["min_price"], collection[0][2]))
#
#        if len(collection[1][2]) == 0:
#            collection[1][2] = price_elem["max_price"]
#        else:
#            collection[1][2] = list(map(add, price_elem["max_price"], collection[1][2]))
#
#        if len(collection[2][2]) == 0:
#            collection[2][2] = price_elem["mean_price"]
#        else:
#            collection[2][2] = list(
#                map(add, price_elem["mean_price"], collection[2][2])
#            )
#
#        # print(price_elem["min_price"][len(price_elem)-1])
#        collection[0][0] = (
#            collection[0][0] + price_elem["min_price"][len(price_elem) - 1]
#        )
#        collection[1][0] = (
#            collection[1][0] + price_elem["max_price"][len(price_elem) - 1]
#        )
#        collection[2][0] = (
#            collection[2][0] + price_elem["mean_price"][len(price_elem) - 1]
#        )
#
#    pdf.cell(60, 10, f"Cards watched: {len(csv_file)}", 0, 1)
#    pdf.cell(60, 10, f"Collection MINimum value: {collection[0][0]} ", 0, 1)
#    pdf.cell(60, 10, f"Collection MEAN value: {collection[1][0]} ", 0, 1)
#    pdf.cell(60, 10, f"Collection MAXimum value: {collection[2][0]} ", 0, 1)
#
#    for elem in collection:
#        None
#
#        plt.figure(figsize=(12, 4))
#        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
#        plt.plot(price_elem["price_date"], elem[2])
#        # TODO check dir
#
#        if os.path.isdir(global_var.custom_dir + "/images/") == False:
#            raise expt.InternalException(
#                "Unable to find directory with name: "
#                + str(global_var.custom_dir + "//images/")
#            )
#            exit(-1)
#        plt.title(f"Collection {elem[1]} price")
#        plt.savefig(
#            f"{global_var.custom_dir}/images/collection_{elem[1].lower()}.png",
#            dpi=300,
#            bbox_inches="tight",
#            pad_inches=0,
#        )
#        plt.close()
#        pdf.image(
#            f"{global_var.custom_dir}/images/collection_{elem[1].lower()}.png",
#            y=pdf.get_y(),
#            h=60,
#        )
#        pdf.ln(70)  # Move down based on width/aspect ratio + 5mm padding
#    pdf.add_page()
#    return 0
#
#
# """
# Generate the general stock page for the general index with commulative information for the stocks
# on all the watched cards
# pdf: the object used to build the pdf document builded with fpdf
# csv_file: the map that contains the information for the cards watched extracted from a csv file
# """
#
#
# def stock_page(pdf, csv_file):
#    collection = [
#        {0: 0, 1: "Stock", 2: []},
#        {0: 0, 1: "Foil", 2: []},
#        {0: 0, 1: "Signed", 2: []},
#        {0: 0, 1: "Altered", 2: []},
#    ]
#    for elem in csv_file:
#        price_elem = drender.render_stock_month(
#            elem, ["stock", "foil", "signed", "altered", "stock_date"]
#        )
#
#        if len(collection[0][2]) == 0:
#            collection[0][2] = price_elem["stock"]
#        else:
#            collection[0][2] = list(map(add, price_elem["stock"], collection[0][2]))
#
#        if len(collection[1][2]) == 0:
#            collection[1][2] = price_elem["foil"]
#
#        else:
#            collection[1][2] = list(map(add, price_elem["foil"], collection[1][2]))
#
#        if len(collection[2][2]) == 0:
#            collection[2][2] = price_elem["signed"]
#        else:
#            collection[2][2] = list(map(add, price_elem["signed"], collection[2][2]))
#
#        if len(collection[3][2]) == 0:
#            collection[3][2] = price_elem["altered"]
#        else:
#            collection[3][2] = list(map(add, price_elem["altered"], collection[3][2]))
#
#        # print(price_elem["min_price"][len(price_elem)-1])
#        collection[0][0] = collection[0][0] + price_elem["stock"][len(price_elem) - 1]
#        collection[1][0] = collection[1][0] + price_elem["foil"][len(price_elem) - 1]
#        collection[2][0] = collection[2][0] + price_elem["signed"][len(price_elem) - 1]
#        collection[3][0] = collection[3][0] + price_elem["altered"][len(price_elem) - 1]
#
#    for elem in collection:
#        plt.figure(figsize=(12, 4))
#        # plt.grid(color="#F2F2F2", alpha=1, order=0)
#        plt.plot(price_elem["stock_date"], elem[2])
#        plt.title(f"{elem[1]} Trend")
#
#        plt.savefig(
#            f"{global_var.custom_dir}/images/collection_{elem[1].lower()}.png",
#            dpi=300,
#            bbox_inches="tight",
#            pad_inches=0,
#        )
#        plt.close()
#        pdf.image(
#            f"{global_var.custom_dir}/images/collection_{elem[1].lower()}.png",
#            y=pdf.get_y(),
#            h=60,
#        )
#        pdf.ln(70)  # Move down based on width/aspect ratio + 5mm padding
#    pdf.add_page()
#    return 0

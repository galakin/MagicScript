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


def card_graph(name, pdf, card_type):
    if pdf.render == True:
        print("...Generating " + card_type + ' graph for: "' + str(name) + '"')

        filter_card_prices = drender.render_prices_month(
            global_var.custom_dir
            + str(name).lower().replace(" ", "/", name.count(""))
            + "_price.csv",
            [
                "date",
                card_type + "_min_price",
                card_type + "_max_price",
                card_type + "_mean_price",
            ],
        )

        pdf.add_page()
        # Centered text in a framed 20*10 mm cell and line break

        pdf.cell(60, 10, "Prices for " + card_type + " " + str(name), 0, 1)

        graph_list = []
        for elem in ["min", "max", "mean"]:
            xaxis = filter_card_prices["date"]

            plt.figure(figsize=(12, 4))
            plt.grid(color="#F2F2F2", alpha=1, zorder=0)
            plt.plot(xaxis, filter_card_prices[card_type + "_" + elem + "_price"])

            path = (
                global_var.custom_dir
                + "/images/"
                + card_type
                + "_"
                + str(name).lower().replace(" ", "/", name.count(""))
            )
            if os.path.isdir(global_var.custom_dir + "/images/") == False:
                raise expt.InternalException(
                    "Unable to find directory with name: "
                    + str(global_var.custom_dir + "/images/")
                )
                exit(-1)
            plt.title(elem + "price")
            plt.savefig(
                path + "_" + elem + ".png", dpi=300, bbox_inches="tight", pad_inches=0
            )
            plt.close()
            graph_list.append(path + "_" + elem + ".png")

        pdf.page_body(graph_list, name)

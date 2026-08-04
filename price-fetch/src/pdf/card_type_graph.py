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
import src.log_msg as logMsg
import src.exceptions as expt
import global_var


def card_graph(card_info, pdf, card_type):
    logMsg.loggin_messages(
        f'...Generating {card_type} graph for: "{str(card_info[0])}"'
    )

    filter_card_prices = drender.render_prices_month(
        card_info,
        [
            "price_date",
            card_type + "_min_price",
            card_type + "_max_price",
            card_type + "_mean_price",
        ],
    )

    pdf.add_page()
    # Centered text in a framed 20*10 mm cell and line break

    pdf.cell(60, 10, "Prices for " + card_type + " " + str(card_info[0]), 0, 1)

    graph_list = []
    for elem in ["min", "max", "mean"]:
        xaxis = filter_card_prices["price_date"]

        plt.figure(figsize=(12, 4))
        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
        plt.plot(xaxis, filter_card_prices[card_type + "_" + elem + "_price"])

        path = (
            global_var.custom_dir
            + "/images/"
            + card_type
            + "_"
            + str(card_info[0]).lower().replace(" ", "_", card_info[0].count(""))
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

    pdf.page_body(graph_list, card_info[0])

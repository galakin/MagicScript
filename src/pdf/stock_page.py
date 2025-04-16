import fpdf
import numpy
import pandas
import os
from datetime import date
from matplotlib import rcParams
import matplotlib.pyplot as plt

import src.rwCsw as rwCsw
import src.stocks as stocks
import src.dateRender as drender
import src.pdf.cardInfo as cardInfo
import src.pdf.card_type_graph as cg
import src.pdf.stock_page as sg
import src.log_msg as logMsg
import src.exceptions as expt
import global_var


def generate_stocks_page(pdf, card_info):
    # Add new page to avoid graph collision
    pdf.add_page()
    logMsg.loggin_messages(f"...Generate {card_info[0]} stock page")
    home_dir = os.getenv("HOME")
    filter_price_csw = drender.render_stock_month(
        card_info, ["stocks", "foil", "signed", "altered", "stock_date"]
    )

    for list_elem in ["stocks", "foil", "signed", "altered"]:
        pass
        # general stock graph
        xaxis = filter_price_csw["stock_date"]
        yaxis = filter_price_csw[list_elem]

        plt.figure(figsize=(12, 4))
        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
        plt.plot(xaxis, yaxis)

        # TODO check dir
        name = (
            global_var.custom_dir
            + "images/"
            + str(card_info[0]).lower().replace(" ", "_", card_info[0].count(""))
        )
        if os.path.isdir(home_dir + "/.priceCsv/images/") == False:
            raise expt.InternalException(
                "Unable to find directory with name: "
                + str(home_dir + "/.priceCsv/images/")
            )
            exit(-1)

        plt.title(card_info[0] + " " + list_elem + " stock")
        plt.savefig(
            name + "_" + list_elem + ".png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0,
        )
        plt.close()

    pdf.page_body(
        [
            name + "_stocks.png",
            name + "_foil.png",
            name + "_signed.png",
            name + "_altered.png",
        ],
        card_info[0],
    )

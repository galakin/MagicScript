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
import global_var


def generate_pdf_report(card_list):
    pdf = PDF()
    pdf.generate_file(card_list)

    rcParams["axes.spines.top"] = False
    rcParams["axes.spines.right"] = False

    pdf.output(global_var.custom_output + "/" + global_var.custom_name, "F")


class PDF(fpdf.FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def generate_file(
        self,
        csv_file,
    ):
        # Generates the report

        self.set_font("Arial")
        self.add_page()
        # Centered text in a framed 20*10 mm cell and line break

        self.cell(60, 10, "Report of cards prices", 0, 1)
        self.cell(60, 10, "Price updated last time at: " + str(date.today()), 0, 1)

        # if render :
        if os.path.exists(global_var.custom_dir + "/images") == False:
            os.mkdir(global_var.custom_dir + "/images")
        is_first_page = True
        for elem in csv_file:
            self.generate_graph(elem, is_first_page)
            for type in global_var.general_graph_type:
                cg.card_graph(elem, self, type)
            sg.generate_stocks_page(self, elem)
            cardInfo.generate_info(self, elem)

            self.add_page()
            if is_first_page == True:
                is_first_page = False

    def first_page(self, images, elem):
        if len(images) < 3:
            raise expt.InternalException(
                "Unable to find the correct no of graph images during PDF cretion!"
            )
            exit(-1)
        self.cell(60, 10, "Price for " + str(elem[0]), 0, 1)
        self.image(images[0], 15, 65, self.WIDTH - 30)
        self.image(images[1], 15, self.WIDTH / 2 + 35, self.WIDTH - 30)
        self.image(images[2], 15, self.WIDTH, self.WIDTH - 30)

    def page_body(self, images, elem):
        if len(images) < 3:
            raise expt.InternalException(
                "Unable to find the correct no of graph images during PDF cretion!"
            )
            exit(-1)
        if len(images) == 3:

            self.image(images[0], 15, 50, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 25, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH, self.WIDTH - 30)
        elif len(images) == 4:
            self.cell(60, 10, str(elem) + " stocks", 0, 1)
            self.image(images[0], x=15, y=50, w=self.WIDTH - 80)
            self.image(images[1], 15, (self.WIDTH / 2) - 2, w=self.WIDTH - 80)
            self.image(images[2], 15, self.WIDTH - 50, self.WIDTH - 80)
            self.image(images[3], 15, self.WIDTH + 5, self.WIDTH - 80)

    def generate_graph(self, elem, is_first_page):
        # TODO: add expension code eg 'ONE'

        filter_price_csw = drender.render_prices_month(
            elem,
            ["price_date", "min_price", "max_price", "mean_price"],
        )

        # Generate graph for min price
        xaxis = filter_price_csw["price_date"]
        yaxis1, yaxis2, yaxis3 = (
            filter_price_csw["min_price"],
            filter_price_csw["max_price"],
            filter_price_csw["mean_price"],
        )
        plt.figure(figsize=(12, 4))
        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
        plt.plot(xaxis, yaxis1)

        # TODO check dir
        name = (
            global_var.custom_dir
            + "/images/"
            + str(elem).lower().replace(" ", "/", elem.count(""))
        )
        if os.path.isdir(global_var.custom_dir + "/images/") == False:
            raise expt.InternalException(
                "Unable to find directory with name: "
                + str(global_var.custom_dir + "/images/")
            )
            exit(-1)

        plt.title("minumum price")
        plt.savefig(name + "_min.png", dpi=300, bbox_inches="tight", pad_inches=0)
        plt.close()

        # Generate graph for max price
        plt.figure(figsize=(12, 4))
        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
        plt.plot(xaxis, yaxis2)
        plt.title("maximum price")
        plt.savefig(name + "_max.png", dpi=300, bbox_inches="tight", pad_inches=0)
        plt.close()

        # Generate graph for mean price
        plt.figure(figsize=(12, 4))
        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
        plt.plot(xaxis, yaxis3)
        plt.title("mean price")
        plt.savefig(name + "_mean.png", dpi=300, bbox_inches="tight", pad_inches=0)
        plt.close()

        if is_first_page == False:
            self.page_body(
                [name + "_min.png", name + "_max.png", name + "_mean.png"], elem
            )
        else:
            self.first_page(
                [name + "_min.png", name + "_max.png", name + "_mean.png"], elem
            )

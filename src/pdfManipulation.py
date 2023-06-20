import fpdf
import numpy
import pandas
import os
from datetime import date
from matplotlib import rcParams
import matplotlib.pyplot as plt

import src.rwCsw as rwCsw
import src.stocks as stocks


def generate_pdf_report(csv_file):
    home_dir = os.getenv("HOME")
    pdf = PDF()
    pdf.generate_file(csv_file)

    rcParams["axes.spines.top"] = False
    rcParams["axes.spines.right"] = False

    if home_dir != None:
        pdf.output("/home/jacopopela/PriceRepot.pdf", "F")
        print("PDF created at index: /home/jacopopela/PriceRepot.pdf")
    else:
        pdf.output(str(home_dir) + "/PriceRepot.pdf", "F")
        print("PDF created at index: ", str(home_dir) + "/PriceRepot.pdf")


class PDF(fpdf.FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def header(self):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        self.set_font("Arial", "B", 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, "Price report", 0, 0, "R")

        self.ln(20)

    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, "Page " + str(self.page_no()), 0, 0, "C")

    def generate_file(self, csv_file):
        # Generates the report
        self.add_page()
        # Centered text in a framed 20*10 mm cell and line break
        self.cell(60, 10, "Report of cards prices", 0, 1)
        self.cell(60, 10, "Price updatae at: " + str(date.today()), 0, 1)

        home_dir = os.getenv("HOME")
        if os.path.exists(home_dir + "/.priceCsv/images") == False:
            os.mkdir(home_dir + "/.priceCsv/images")
        is_first_page = True
        for elem in csv_file:
            self.generate_graph(elem, is_first_page)
            self.generate_stocks_page(elem)
            self.add_page()
            if is_first_page == True:
                is_first_page = False

    def first_page(self, images, elem):
        if len(images) < 3:
            raise Exception(
                "Unable to find the correct no of graph images during PDF cretion!"
            )
            exit(-1)
        self.cell(60, 10, "Price for " + str(elem), 0, 1)
        self.image(images[0], 15, 65, self.WIDTH - 30)
        self.image(images[1], 15, self.WIDTH / 2 + 35, self.WIDTH - 30)
        self.image(images[2], 15, self.WIDTH, self.WIDTH - 30)

    def analisys_page(self, elem, prices):
        print("mario")
        # TODO define analisys page body

    def page_body(self, images, elem):
        if len(images) < 3:
            raise Exception(
                "Unable to find the correct no of graph images during PDF cretion!"
            )
            exit(-1)
        if len(images) == 3:
            self.cell(60, 10, "Price for " + str(elem), 0, 1)
            # self.cell()
            self.image(images[0], 15, 50, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 25, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH, self.WIDTH - 30)
        elif len(images) == 4:
            self.cell(60, 10, str(elem) + " stocks", 0, 1)
            self.image(images[0], x=15, y=50, w=self.WIDTH - 80)
            self.image(images[1], 15, (self.WIDTH / 2) - 2, w=self.WIDTH - 80)
            self.image(images[2], 15, self.WIDTH - 50, self.WIDTH - 80)
            self.image(images[3], 15, self.WIDTH + 5, self.WIDTH - 80)

    def generate_stocks_page(self, elem):
        # Add new page to avoid graph collision
        self.add_page()
        print("...Generate " + elem + " stock page")
        home_dir = os.getenv("HOME")
        price_csw = rwCsw.read_csv(
            "/.priceCsv/"
            + str(elem).lower().replace(" ", "/", elem.count(""))
            + "_stock.csv"
        )

        for list_elem in ["stock", "foil", "signed", "altered"]:

            # general stock graph
            xaxis = price_csw["date"]
            yaxis = price_csw[list_elem]

            plt.figure(figsize=(12, 4))
            plt.grid(color="#F2F2F2", alpha=1, zorder=0)
            plt.plot(xaxis, yaxis)

            # TODO check dir
            name = (
                home_dir
                + "/.priceCsv/images/"
                + str(elem).lower().replace(" ", "/", elem.count(""))
            )
            if os.path.isdir(home_dir + "/.priceCsv/images/") == False:
                raise Exception(
                    "Unable to find directory with name: "
                    + str(home_dir + "/.priceCsv/images/")
                )
                exit(-1)

            plt.title(elem + " " + list_elem + " stock")
            plt.savefig(
                name + "_" + list_elem + ".png",
                dpi=300,
                bbox_inches="tight",
                pad_inches=0,
            )
            plt.close()

        self.page_body(
            [
                name + "_stock.png",
                name + "_foil.png",
                name + "_signed.png",
                name + "_altered.png",
            ],
            elem,
        )

    def generate_graph(self, elem, is_first_page):
        # TODO: add expension code eg 'ONE'
        home_dir = os.getenv("HOME")
        price_csw = rwCsw.read_csv(
            "/.priceCsv/"
            + str(elem).lower().replace(" ", "/", elem.count(""))
            + "_price.csv"
        )

        # Generate graph for min price
        xaxis = price_csw["date"]
        yaxis1, yaxis2, yaxis3 = (
            price_csw["min_price"],
            price_csw["max_price"],
            price_csw["mean_price"],
        )
        plt.figure(figsize=(12, 4))
        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
        plt.plot(xaxis, yaxis1)

        # TODO check dir
        name = (
            home_dir
            + "/.priceCsv/images/"
            + str(elem).lower().replace(" ", "/", elem.count(""))
        )
        if os.path.isdir(home_dir + "/.priceCsv/images/") == False:
            raise Exception(
                "Unable to find directory with name: "
                + str(home_dir + "/.priceCsv/images/")
            )
            exit(-1)

        plt.savefig(name + "_min.png", dpi=300, bbox_inches="tight", pad_inches=0)
        plt.title("minumum price")
        plt.close()

        # Generate graph for max price
        plt.figure(figsize=(12, 4))
        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
        plt.plot(xaxis, yaxis2)
        plt.savefig(name + "_max.png", dpi=300, bbox_inches="tight", pad_inches=0)
        plt.title("maximum price")
        plt.close()

        # Generate graph for mean price
        plt.figure(figsize=(12, 4))
        plt.grid(color="#F2F2F2", alpha=1, zorder=0)
        plt.plot(xaxis, yaxis3)
        plt.savefig(name + "_mean.png", dpi=300, bbox_inches="tight", pad_inches=0)
        plt.title("mean price")
        plt.close()

        if is_first_page == False:
            self.page_body(
                [name + "_min.png", name + "_max.png", name + "_mean.png"], elem
            )
        else:
            self.first_page(
                [name + "_min.png", name + "_max.png", name + "_mean.png"], elem
            )

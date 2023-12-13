import sys

# from .. import src.connection as nwrk
import sys
import os
import pytest

import connection as nwrk
import dateRender as date
import exceptions as expt
import rwCsw as csv
import connection as con
import priceCard as price
import stocks as stocks


def test_date_render():
    assert date.render_prices_month(None, []) == None
    assert date.render_prices_month("", []) == None

    f = open("test_csv.csv", "w")
    f.write("data,prices\n0,0")
    f.close()
    assert date.render_prices_month("test_csv.csv", []) == None
    os.remove("test_csv.csv")


def test_csv():
    HOME = os.getenv("HOME")
    os.environ["HOME"] = ""
    # with pytest.raises(ValueError, match=r".* 123 .*"):
    # myfunc()
    # csv.write_main_dir()

    with pytest.raises(Exception, match=r".*csv.*"):
        csv.read_csv("test")
    os.environ["HOME"] = HOME

    with pytest.raises(Exception, match=r".*csv.*"):
        csv.read_csv("test")

    os.environ["HOME"] = ""
    with pytest.raises(Exception, match=r".*HOME.*"):
        csv.search_row("test", "test", "test", log=False)
    os.environ["HOME"] = HOME

    with pytest.raises(Exception, match=r".*Unable to find csv.*"):
        csv.search_row("test", "test", "test", log=False)
    # TODO: check that search row method found the correct index


def test_connection():
    with pytest.raises(Exception, match=r".*No scheme.*"):
        con.verify_connection("test", "test")

    base_url = "https://api.cardtrader.com/api/v2"
    database_url = "https://api.scryfall.com"

    if os.getenv("AUTH_TOKEN") != None:
        auth_token = os.getenv("AUTH_TOKEN")
        headers = {"Authorization": auth_token}

        assert con.verify_connection(base_url, headers) == True

        with pytest.raises(Exception, match=r".*unable to fetch.*"):
            con.search_for_card("NO_CARD", database_url, base_url, headers)

        assert con.search_for_card("Duress", database_url, base_url, headers)

        with pytest.raises(Exception, match=r".*Invalid URL.*"):
            con.search_for_card("Duress", "no_db", base_url, headers)

        with pytest.raises(Exception, match=r".*Invalid URL.*"):
            con.search_for_card("Duress", database_url, "no_base_url", headers)

        assert con.search_for_card("Duress", database_url, base_url, {}) == False


def test_price_card():
    with pytest.raises(Exception, match=r".*Unable.*fetch seller.*"):
        price.extract_default([], None)

    with pytest.raises(Exception, match=r".*Item tag.*isn't.*correctly.*"):
        price.extract_default(["a", "b"], None)

    with pytest.raises(Exception, match=r".*Item tag.*isn't.*correctly.*"):
        price.extract_default(["a", "b"], "")

    with pytest.raises(Exception, match=r".*Item tag.*isn't.*correctly.*"):
        price.extract_default(["a", "b"], "    ")

    with pytest.raises(Exception, match=r".*Unable.*fetch seller.*"):
        price.get_prices([], None)

    with pytest.raises(Exception, match=r".*Item tag.*isn't.*correctly.*"):
        price.get_prices(["a", "b"], None)

    with pytest.raises(Exception, match=r".*Item tag.*isn't.*correctly.*"):
        price.get_prices(["a", "b"], "")

    with pytest.raises(Exception, match=r".*Item tag.*isn't.*correctly.*"):
        price.get_prices(["a", "b"], "    ")


def test_stocks():
    with pytest.raises(Exception, match=r".*Unable.*fetch seller.*"):
        stocks.finds_stocks([], None)

    with pytest.raises(Exception, match=r".*Item tag.*isn't.*correctly.*"):
        stocks.finds_stocks(["a", "b"], None)

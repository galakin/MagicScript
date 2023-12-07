import sys

# from .. import src.connection as nwrk
import sys
import os

import connection as nwrk
import dateRender as date


def test_date_render():
    assert date.render_prices_month(None, []) == None
    assert date.render_prices_month("", []) == None

    f = open("test_csv.csv", "w")
    f.write("data,prices\n0,0")
    f.close()
    assert date.render_prices_month("test_csv.csv", []) == None
    os.remove("test_csv.csv")

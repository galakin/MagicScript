import pandas
import datetime

import src.exceptions as expt
import src.rwCsw as rwCsw


def render_prices_month(path, list_elem):
    print("...render latest month prices")
    tod = datetime.datetime.now().date()
    delta = datetime.timedelta(days=30)
    time_range = tod - delta

    csv_file = pandas.read_csv(path)

    valid_date = pandas.DataFrame()

    data = {}
    for elem in list_elem:
        data[elem] = []
    first_elem, elem_delta = 0, 0

    for elem in range(len(csv_file["date"])):
        # print(csv_file["date"])
        # print(csv_file["date"][elem])
        if csv_file["date"][elem] != 0:
            csv_date = datetime.datetime.strptime(
                str(csv_file["date"][elem]), "%Y-%m-%d"
            ).date()
            if time_range < csv_date:

                tmp_dict = csv_file.iloc[[elem]].to_dict()
                if len(tmp_dict["date"].keys()) == 1 and first_elem == 0:
                    first_elem = list(tmp_dict["date"].keys())[0]

                if valid_date.empty:
                    for index in range(len(list_elem)):
                        data[list_elem[index]] = [
                            tmp_dict.get(list_elem[index]).get(first_elem)
                        ]
                    valid_date = pandas.DataFrame.from_dict(data)
                else:
                    for index in range(len(list_elem)):
                        data[list_elem[index]] = tmp_dict.get(list_elem[index]).get(
                            first_elem
                        )
                    valid_date.loc[len(valid_date.index)] = data
                first_elem += 1

    # print("valid date: " + str(len(valid_date.index)))

    return valid_date


def render_stock_month(path):
    print("...render latest month stock")
    tod = datetime.datetime.now().date()
    delta = datetime.timedelta(days=30)
    time_range = tod - delta

    csv_file = pandas.read_csv(path)

    valid_date = pandas.DataFrame()
    # valid_date.columns = ['date', 'stock', 'foil', 'signed', 'altered']
    for elem in range(len(csv_file["date"])):
        csv_date = datetime.datetime.strptime(csv_file["date"][elem], "%Y-%m-%d").date()
        if time_range < csv_date:
            tmp_dict = csv_file.iloc[[elem]].to_dict()
            date = tmp_dict.get("date").get(elem)
            stock = tmp_dict.get("stock").get(elem)
            foil = tmp_dict.get("foil").get(elem)
            signed = tmp_dict.get("signed").get(elem)
            altered = tmp_dict.get("altered").get(elem)
            data = {
                "date": [date],
                "stock": [stock],
                "foil": [foil],
                "signed": [signed],
                "altered": [altered],
            }

            if valid_date.empty:
                valid_date = pandas.DataFrame.from_dict(data)
            else:
                valid_date.loc[len(valid_date.index)] = {
                    "date": date,
                    "stock": stock,
                    "foil": foil,
                    "signed": signed,
                    "altered": altered,
                }

    # print("valid date: " + str(len(valid_date.index)))

    return valid_date

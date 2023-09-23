import src.exceptions as expt


def get_prices(seller_list, item_tag):
    # IDEA: item list are in increasing pricing order, the first elem is the
    # cheapest one, the latest elem is the more expensive one
    try:
        extract_map = extract_default(seller_list, item_tag)
        default_list = extract_map["default_list"]
        foil_list = extract_map["foil_list"]
        signed_list = extract_map["signed_list"]
        altered_list = extract_map["altered_list"]
        mean_price = 0
        for elem in default_list:
            mean_price += elem["price_cents"] / 100
        mean_price = mean_price / len(default_list)
        tmp_map = {
            "min_price": default_list[0]["price_cents"] / 100,
            "max_price": default_list[len(default_list) - 1]["price_cents"] / 100,
            "mean_price": mean_price,
            "foil_min_price": foil_list[0]["price_cents"] / 100,
            "foil_max_price": foil_list[len(foil_list) - 1]["price_cents"] / 100,
            "signed_min_price": signed_list[0]["price_cents"] / 100
            if len(signed_list) > 0
            else 0,
            "signed_max_price": signed_list[len(signed_list) - 1]["price_cents"] / 100
            if len(signed_list) > 0
            else 0,
            "altered_min_price": altered_list[0]["price_cents"] / 100
            if len(altered_list) > 0
            else 0,
            "altered_max_price": altered_list[len(altered_list) - 1]["price_cents"]
            / 100
            if len(altered_list) > 0
            else 0,
        }

        # Calculate foil mean price
        mean_price = 0
        for elem in foil_list:
            mean_price += elem["price_cents"] / 100
        mean_price = mean_price / len(foil_list)
        tmp_map["foil_mean_price"] = mean_price

        # Calculate signed mean price
        mean_price = 0
        if len(signed_list) > 0:
            for elem in signed_list:
                mean_price += elem["price_cents"] / 100
            mean_price = mean_price / len(default_list)
        tmp_map["signed_mean_price"] = mean_price

        # Calculate altered mean price
        mean_price = 0
        if len(altered_list) > 0:
            for elem in altered_list:
                mean_price += elem["price_cents"] / 100
            mean_price = mean_price / len(altered_list)
        tmp_map["altered_mean_price"] = mean_price
        return tmp_map
    except expt.InternalException as ex:
        print(ex)
        print("env, item_tag: ", item_tag)
        print("seller list: " + str(seller_list[item_tag][0]))
        exit(-1)


# Extract the price for the `default` item, where default means no foil, nor signed or altered
def extract_default(seller_list, item_tag):
    default_list, foil_list, signed_list, altered_list = [], [], [], []
    for elem in range(len(seller_list[item_tag])):
        if (
            seller_list[item_tag][elem]["properties_hash"]["signed"] == False
            and seller_list[item_tag][elem]["properties_hash"]["mtg_foil"] == False
            and seller_list[item_tag][elem]["properties_hash"]["altered"] == False
        ):
            default_list.append(seller_list[item_tag][elem])
        if (
            seller_list[item_tag][elem]["properties_hash"]["signed"] == False
            and seller_list[item_tag][elem]["properties_hash"]["mtg_foil"] == True
            and seller_list[item_tag][elem]["properties_hash"]["altered"] == False
        ):
            foil_list.append(seller_list[item_tag][elem])
        if seller_list[item_tag][elem]["properties_hash"]["signed"] == True:
            signed_list.append(seller_list[item_tag][elem])
        if seller_list[item_tag][elem]["properties_hash"]["altered"] == True:
            altered_list.append(seller_list[item_tag][elem])

    # properties_hash
    # print(seller_list[item_tag][0])

    return {
        "default_list": default_list,
        "foil_list": foil_list,
        "signed_list": signed_list,
        "altered_list": altered_list,
    }

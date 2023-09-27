import src.exceptions as expt


def get_prices(seller_list, item_tag):
    # IDEA: item list are in increasing pricing order, the first elem is the
    # cheapest one, the latest elem is the more expensive one
    # TODO: check error here!
    try:
        default_list = extract_default(seller_list, item_tag)
        min_price = default_list[0]["price_cents"] / 100
        mean_price = 0
        for elem in default_list:
            mean_price += elem["price_cents"] / 100
            # TODO check elem validity for foil/custom/
        mean_price = mean_price / len(default_list)
        max_price = default_list[len(default_list) - 1]["price_cents"] / 100
        print(
            "min_price: "
            + str(min_price)
            + "\tmax_price: "
            + str(max_price)
            + "\tmean_price: "
            + str(mean_price)
        )
        return {
            "min_price": min_price,
            "max_price": max_price,
            "mean_price": mean_price,
        }
    except expt.InternalException as ex:
        print(ex)
        print("env, item_tag: ", item_tag)
        print("seller list: " + str(seller_list[item_tag][0]))
        exit(-1)


# Extract the price for the `default` item, where default means no foil, nor signed or altered
def extract_default(seller_list, item_tag):
    default_list = []
    for elem in range(len(seller_list[item_tag])):
        if (
            seller_list[item_tag][elem]["properties_hash"]["signed"] == False
            and seller_list[item_tag][elem]["properties_hash"]["mtg_foil"] == False
            and seller_list[item_tag][elem]["properties_hash"]["altered"] == False
        ):
            default_list.append(seller_list[item_tag][0])
    print("default list length: " + str(len(default_list)))
    # properties_hash
    # print(seller_list[item_tag][0])

    return default_list

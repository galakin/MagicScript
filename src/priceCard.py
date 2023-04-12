def get_prices(seller_list, item_tag):
    # IDEA: item list are in increasing pricing order, the first elem is the
    # cheapest one, the latest elem is the more expensive one
    # TODO: check error here!
    try:
        min_price = seller_list[item_tag][0]["price_cents"] / 100
        mean_price = 0
        for elem in seller_list[item_tag]:
            mean_price += elem["price_cents"] / 100
            # TODO check elem validity for foil/custom/
        mean_price = mean_price / len(seller_list[item_tag])
        max_price = (
            seller_list[item_tag][len(seller_list[item_tag]) - 1]["price_cents"] / 100
        )
        return {
            "min_price": min_price,
            "max_price": max_price,
            "mean_price": mean_price,
        }
    except Exception as ex:
        print(ex)
        print("env, item_tag: ", item_tag)
        print("seller list: " + str(seller_list[item_tag][0]))
        exit(-1)

import requests
import os
import pathlib
import pandas #TODO: change import location 
import json

base_url = "https://api.cardtrader.com/api/v2"
game = "Magic"
category = "Single Cards"

headers = {"Authorization": auth_token}

database_url="https://api.scryfall.com"

print("Fetching auth token...")
#print("auth token env: ", os.getenv("AUTH_TOKEN"))
if os.getenv("AUTH_TOKEN") != None : 
    auth_token = os.getenv("AUTH_TOKEN")
    print("...Auth token fetched from environment variables")
else: print("...Using the default auth token")

def verify_connection():
    ##Fetch game info
    response = requests.get(base_url+"/info", headers=headers)
    if response.status_code == 200:
        print("...Connection Established!\n")
    else: 
        print("Unable to connet to CardTrader API server\nCheck if your API token is still valid!")
        exit()
    #print(response.json())

def fetch_local_card_data():
    home_dir = os.getenv("HOME")
    if home_dir == None:
        print("Unable to find environment variable named HOME\nplease check if you have defined it")
        exit()
    else:
        file_path = pathlib.Path(home_dir+"/card.csv")
        if file_path.is_file():
            print("Card file found!")
        else: 
            print("ERROR: Unable to fin the card file a the default location!")
            exit()
    return True

#TODO: rename module
def preliminary_action():
    found_game = False
    if fetch_local_card_data():
        response = requests.get(base_url+"/games", headers=headers)  
        #print(response.json()['array'])
        for elem in response.json()['array']:
            if elem['name'] == game: 
                print('Selected game found!')
                found_game = True
        if found_game == False:
            print("ERROR: Unable to find selected Game")
            exit()
    return True

def read_csv():
    home_dir = os.getenv("HOME")
    if home_dir != None:
        csv_file = pandas.read_csv("/home/jacopopela/card.csv")
    return csv_file

def search_for_card(name):
    blueprint_id=-1
    expansion_id = -1
    
    card_json = requests.get(database_url+"/cards/named?exact="+name)
    if card_json.status_code != 200: exit()
    scryfall_id = card_json.json()['id'] 
    card_expansion_code = card_json.json()['set']
    expansion_code = requests.get(base_url+"/expansions", headers=headers)
    if expansion_code.status_code != 200: exit()
    
    print("...Retrived the list of expansions")
    for elem in expansion_code.json():
        if elem['code'] == card_expansion_code:
            if expansion_id > 0: exit()
            expansion_id = elem['id']
            print("...Card code found!")
    #retrive card blueprint

    card_blueprint = requests.get(base_url+"/blueprints/export?expansion_id="+str(expansion_id), headers=headers)
    if card_blueprint.status_code != 200: 
        print("ERROR: unable to fetch expensions card")
        exit()

    for elem in card_blueprint.json():
        if elem['name'] == name:
            if blueprint_id > 0: 
                print("ERROR: two product with the same name found")
                exit()
            blueprint_id=elem['id']
            print("card found")

    selled_cards =  requests.get(base_url+"/marketplace/products?blueprint_id="+str(blueprint_id), headers=headers)
    tst = list(selled_cards.json().keys())
    #print(selled_cards.json()[tst[0]][0]['price_cents']/100)
    get_prices(selled_cards.json(), tst[0])
    #Use keys 'price_cents' to fetch the price of the selected card

def get_prices(seller_list, item_tag):
    #IDEA: item list are in increasing pricing order, the first elem is the 
    #cheapest one, the latest elem is the more expensive one 
    print("...feteching prices info")
    cheapest_price = seller_list[item_tag][0]['price_cents']/100
    print("Cheapest card: ",cheapest_price)
    mean_price = 0
    for elem in seller_list[item_tag]:
        #if mean_price == 0: print("price: ",elem['price_cents'])
        mean_price += elem['price_cents']
        #TODO check elem validity for foil/custom/
    mean_price = mean_price / len(seller_list[item_tag])  
    print("card mean price: ", mean_price)


verify_connection()
if preliminary_action(): 
    print("Fetching card info...")
    csv_file = read_csv()
    #print(len(csv_file))
    for elem in range(len(csv_file['card'])):
        if elem == 0: search_for_card(csv_file['card'][elem])





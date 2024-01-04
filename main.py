import requests
import os
import pathlib
import pandas
import json
import argparse
import sys

import connect

# Check if configuration exist
def check_config():
    home_dir = os.getenv("HOME")
    if home_dir == None:
        raise expt.InternalException(
            "Unable to find environment variable named HOME\nplease check if you have defined it"
        )
    if os.path.exists(home_dir + "/.config/magicscript"):
        return True
    else:
        print(
            'Unable to fing config file\nConfig script with "--config" flags or use "--config-file"'
        )
        return False


# Create and populate magicscript config file
def config_script():
    check_semantic = False
    config_map = {}
    home_dir = os.getenv("HOME")
    if home_dir == None:
        raise expt.InternalException(
            "Unable to find environment variable named HOME\nplease check if you have defined it"
        )
    print("Start config script")
    if os.path.exists(home_dir + "/.config/magicscript") == False:
        os.mkdir(home_dir + "/.config/magicscript")
    while check_semantic == False:
        default_dir = input(
            "Use default dir [" + home_dir + "/.priceCsv/] for store card info? [Y/n]: "
        )
        if default_dir.lower() == "y" or default_dir.lower() == "n":
            check_semantic = True
        else:
            print('Please enter "Y" or "n"')
    if default_dir.lower() == "n":
        check_semantic = False
        while check_semantic == False:
            config_map["custom_dir"] = input("Enter config path's dir: ")
            if os.path.exists(config_map["custom_dir"]) == False:
                print(
                    'Unable to find dir "'
                    + config_map["custom_dir"]
                    + '" check if directory exist and enter it again'
                )
            else:
                check_semantic = True
    else:
        config_map["custom_dir"] = home_dir + "/.priceCsv/"

    if os.path.exists(config_map["custom_dir"] + "/.priceCsv"):
        print('...hidden "priceCsv" dir already exist')
    else:
        os.mkdir(config_map["custom_dir"])
        print("...Created storage dir")

    f = open(home_dir + "/.config/magicscript/config.yaml", "w")
    f.write('custom_dir: "' + config_map["custom_dir"] + '"\n')

    # Set output's pdf path
    check_semantic = False
    while check_semantic == False:
        prompt_input = input(
            "Use default dir [" + home_dir + "] for output's pdf file? [Y/n]: "
        )
        if prompt_input.lower() == "y" or prompt_input.lower() == "n":
            check_semantic = True
        else:
            print('Please enter "Y" or "n"')

    config_map["custom_output"] = home_dir
    if prompt_input.lower() == "n":
        check_semantic = False
        while check_semantic == False:
            config_map["custom_output"] = input("Enter output's pdf path: ")
            if os.path.exists(config_map["custom_output"]) == False:
                print(
                    'Unable to find dir "'
                    + config_map["custom_output"]
                    + '" check if directory exist and enter it again'
                )
            else:
                check_semantic = True
    f.write('custom_output: "' + config_map["custom_output"] + '"\n')

    # Set output's pdf name
    check_semantic = False
    while check_semantic == False:
        prompt_input = input(
            'Use default name ["PriceRepot.pdf"] for output\'s pdf? [Y/n]: '
        )
        if prompt_input.lower() == "y" or prompt_input.lower() == "n":
            check_semantic = True
        else:
            print('Please enter "Y" or "n"')

    config_map["custom_name"] = "PriceReport.pdf"
    if prompt_input.lower() == "n":
        print(
            "NOTE: If you enter a file's name that already exits it will be overwrite!"
        )
        config_map["custom_name"] = input("Enter output's pdf file's name: ")
    f.write('custom_name: "' + config_map["custom_name"] + '"\n')

    check_semantic = False
    while check_semantic == False:
        storage_method = input("Storage method [csv/mongo]: ")
        if storage_method.lower() == "csv" or storage_method.lower() == "mongo":
            check_semantic = True
        else:
            print('Please enter "csv" or "mongo"')
    f.write('storage_method: "' + storage_method + '"\n')

    # set fetch info rate
    f.write('fetch_rate: "daily"\n')
    f.close()
    print(
        '...Wrote config to "'
        + home_dir
        + '/.config/magicscript/config.yaml" directory'
    )


if __name__ == "__main__":
    render = True
    ext_env = sys.argv
    # print("env vars: "+str(ext_env))

    if len(ext_env) == 1:
        if check_config():
            connect.main()

    elif any(item in sys.argv for item in sys.argv if item == "--help"):
        print(
            "Welocome to Magic Script, a python script to scrape and collect info"
            + " from the famous Card Trader web site!\nThe following is a list of flags"
            + ' supported by the script:\n - "--quiet": suppress the pdf creation\n -'
            + ' "--config  ": set the script config\n - "--config-file": pass the config'
            + " file directly to the script"
        )
        exit()

    elif any(item in sys.argv for item in sys.argv if item == "--config"):
        print("Configurate Magic Script")
        config_script()
        exit()

    elif any(item in sys.argv for item in sys.argv if item == "--quiet"):
        render = False
        if check_config():
            connect.main(render)

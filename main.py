import requests
import os
import pathlib
import pandas
import json
import argparse
import sys

import connect


def check_config():
    return True


if __name__ == "__main__":
    if check_config():
        render = True
        ext_env = sys.argv
        # print("env vars: "+str(ext_env))

        if len(ext_env) == 1:
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
            exit()

        elif any(item in sys.argv for item in sys.argv if item == "--quiet"):
            render = False

        connect.main(render)
    else:
        print('Config script with "--config" flags or use "--config-file"')

import json
import sys
import yaml
import os
from datetime import datetime
import calendar
import mysql.connector

import src.exceptions as expt
import global_var
import mysql_connect
import src.log_msg as logMsg
import src.cleanup.clean_price as cleanPrice


def retrieve_credentials(username, password):
    retrieved_credentials = get_credentials()
    if retrieved_credentials[0] != None:
        username = retrieved_credentials[0]
    else:
        username = "root"
    if retrieved_credentials[1] != None:
        password = retrieved_credentials[1]
    else:
        password = "cul5ai2xnsgs"

    return (username, password)


def get_credentials():
    logMsg.loggin_messages("Retrieve database credentials")
    try:
        username = os.getenv("MAGIC_DB_USERNAME")
        password = os.getenv("MAGIC_DB_PASSWORD")
        if username == None:
            item_count = 0
            stop_loop = False
            for item in sys.argv:
                if not stop_loop:
                    item_count += 1
                    if item == "--dbuser":
                        stop_loop = True
            if stop_loop:
                username = sys.argv[item_count + 1]
        if password == None:
            item_count = 0
            stop_loop = False
            for item in sys.argv:
                if not stop_loop:
                    item_count += 1
                    if item == "--dbpassword":
                        stop_loop = True
            if stop_loop:
                password = sys.argv[item_count + 1]
        return [username, password]

    except Exception as e:
        print(e)
        return -1

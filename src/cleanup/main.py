import json
import sys
import yaml
import os
import mysql.connector

import src.exceptions as expt
import global_var
import mysql_connect
import src.log_msg as logMsg

"""
Start the Database cleanup process that remove entry older than 3 month
"""


def main():
    username = ""  # database username
    password = ""  # database password
    logMsg.loggin_messages("Starting the Database cleanup process")

    retrieved_credentials = get_credentials()
    if retrieved_credentials[0] != None:
        username = retrieved_credentials[0]
    else:
        username = "root"
    if retrieved_credentials[1] != None:
        password = retrieved_credentials[1]
    else:
        password = "cul5ai2xnsgs"
    database = mysql.connector.connect(
        host="localhost", user=username, password=password
    )

    mycursor = database.cursor()
    mycursor.execute("USE cards_database;")
    return 0


"""
retrive the database credentials either by environment variable, command line variable or by default setting
"""


def get_credentials():
    logMsg.loggin_messages("Retrieve database credentials")
    try:
        username = os.environ("MAGIC_DB_USERNAME")
        password = os.environ("MAGIC_DB_PASSWORD")
        if username == None:
            item_count = 0
            stop_loop = False
            for item in sys.argv and not stop_loop:
                item_count += 1
                if item == "--dbuser":
                    stop_loop = True
            username = sys.argv[item_count + 1]
        if password == None:
            item_count += 1
            stop_loop = False
            for item in sys.argv and not stop_loop:
                if item == "--dbpassword":
                    stop_loop = True
            password = sys.argv[item_count + 1]
        reteurn[username, password]

    except exception:
        print(exception)
        return -1

import json
import sys
import yaml

import src.exceptions as expt
import global_var
import mysql_connect
import src.log_msg as logMsg

"""
Start the Database cleanup process that remove entry older than 3 month
"""


def main():
    logMsg.loggin_messages("Starting the Database cleanup process")
    return 0

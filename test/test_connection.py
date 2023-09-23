import sys

# from .. import src.connection as nwrk
import sys
import os

sys.path.insert(0, "..")
import src.connection as nwrk

total_test = 0
successfull_test = 0


def test_connection():
    tst = test_verify_connection()
    global total_test, successfull_test
    total_test += tst[0]
    successfull_test += tst[1]
    return {"total": total_test, "successfull": successfull_test}


def test_verify_connection():
    test = 0
    successfull = 0
    print('...testing "verify_connection" method')
    try:
        nwrk.verify_connection("", "")
    except:
        test += 1
        successfull += 1

    else:
        test += 1

    try:
        nwrk.verify_connection("https://api.cardtrader.com/api/v2", "")
    except:
        test += 1
        successfull += 1
    else:
        test += 1

    if os.getenv("AUTH_TOKEN") != None:
        auth_token = os.getenv("AUTH_TOKEN")
        headers = {"Authorization": auth_token}
        try:
            nwrk.verify_connection("https://api.cardtrader.com/api/v2", headers=headers)
        except:
            test += 1
        else:
            test += 1
            successfull += 1
    return [test, successfull]

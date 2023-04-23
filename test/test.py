test_threshold = 90

import test_connection as connection

total_test = 0
successful_test = 0

print("start testing ...")
print("...test connection module")
connection_tst = connection.test_connection()
print(
    "total test: ",
    connection_tst["total"],
    "successfull test: ",
    connection_tst["successfull"],
)

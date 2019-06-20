#!/usr/bin/env python
import os
import json_to_discourse
from time import sleep
import sys
import csv_db_funcs
import json
import unit_tests
import interface_discourse


interface_instance_test = interface_discourse.discourse_interface(
    QUIET_MODE=True,
    PATH_TO_SAMPLES_CSV="./sampleresponses.csv",
    TEST_MODE=True,
    TEST_MODE_DEFAULT_EMPTY=True,
)
error_logs = "./errors.csv"
error_logs_test = "./errors_alt.csv"
json_to_discourse.DISCOURSE_DB = "./discourse_test.db"
"""
for root, dirs, files in os.walk(sys.argv[1]):
    for img in files:
        print(img)
        my_json = None
        with open(os.path.join(sys.argv[1],img), "r") as my_json_file:
            my_json = json.load(my_json_file)
        try:
            unit_tests.sample_json_test(my_json, interface_instance_test)
        except NotImplementedError as e:
            csv_db_funcs.append_data(
                img, str(e), error_logs_test, [my_json], append=True
            )
            os.remove(os.path.join(sys.argv[1],img))

print("Unit test finished")
print("Exiting...")
sys.exit(0)"""
interface_instance = interface_discourse.discourse_interface(QUIET_MODE=True)
json_to_discourse.DISCOURSE_DB = "./discourse_db.db"
for root, dirs, files in os.walk(sys.argv[1]):
    for img in files:
        print(img)
        my_json = None
        with open(os.path.join(sys.argv[1], img), "r") as my_json_file:
            my_json = json.load(my_json_file)
        try:
            json_to_discourse.process_json(interface_instance, my_json, skip=False)
        except NotImplementedError as e:
            if interface_instance.LAST_RES is not None:
                csv_db_funcs.store(
                    img,
                    str(e),
                    [interface_instance.LAST_RQST, interface_instance.LAST_RES.json()],
                    error_logs,
                )
            else:
                csv_db_funcs.store(
                    img,
                    str(e),
                    [interface_instance.LAST_RQST, "No Response"],
                    error_logs,
                )
            print(">>>>>>>>>>>>>>")
            print("Deleting {}".format(img))
            print(">>>>>>>>>>>>>>")
        os.remove(os.path.join(sys.argv[1], img))

# except Exception as e:
#     print("ERROR")
#     if interface_instance.LAST_RES is not None:
#         csv_db_funcs.store(
#             img, str(e), [interface_instance.LAST_RES.json()], error_logs
#         )
#     else:
#         csv_db_funcs.store(img, str(e), ["No Response"], error_logs)
#     continue
# os.remxoxoove(img)
# try:
#     json_to_discourse.process_json(interface_instance, my_json)
#     os.remove(img)
# except Exception as e:
#     print("ERROR ERROR")
#     print(img)
#     if interface_instance.LAST_RES is not None:
#         csv_db_funcs.store(
#             img, str(e), [interface_instance.LAST_RES.json()], error_logs
#         )
#     else:
#         csv_db_funcs.store(img, str(e), ["No Response"], error_logs)
#     continue

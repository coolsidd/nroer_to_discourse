#!/usr/bin/env python
import types
import interface_discourse
import json_to_discourse
import csv_db_funcs
import ast
import json
from pprint import pprint

PATH_TO_GANDHI_JSON = "./gandhi.json"
PATH_TO_POLITICAL_JSON = "./politics.json"
PATH_TO_SAMPLES_CSV = "./sampleresponses.csv"


def multiline_input(display_text):
    print(display_text)
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    text = "\n".join(lines)
    return text


def setup_samples():
    k = input("Press q to quit. Any other key to start\n")
    funcs = get_funtions(interface_discourse.discourse_interface)
    for func in funcs:
        while True:
            if csv_db_funcs.identify("samples", func.__name__, PATH_TO_SAMPLES_CSV):
                print("The current dict:")
                pprint(
                    csv_db_funcs.identify("samples", func.__name__, PATH_TO_SAMPLES_CSV)
                )

            k = multiline_input(
                """Sample for function: {}
s to skip\nq to quit\nc to clear\n""".format(
                    func.__name__
                )
            )
            if k == "s":
                break
            elif k == "":
                continue
            elif k == "q":
                return
            elif k == "c":
                csv_db_funcs.store(
                    "samples", func.__name__, [], PATH_TO_SAMPLES_CSV, override=True
                )
                break
            else:
                try:
                    k = dict(json.loads(k))
                    pprint(k)
                    ast.literal_eval(str(k))
                    csv_db_funcs.store(
                        "samples",
                        func.__name__,
                        str(k),
                        PATH_TO_SAMPLES_CSV,
                        override=True,
                    )
                    break
                except Exception as e:
                    print(e)
                    print("That dict doesn't seem to be valid")
                    continue


def get_funtions(module):
    return [
        getattr(module, a)
        for a in dir(module)
        if isinstance(getattr(module, a), types.FunctionType)
    ]


def sample_json_test():
    interface_discourse.TEST_MODE = True
    interface_discourse.TEST_MODE_DEFAULT_EMPTY = False


def mahatma_gandhi_json_test():
    # GET INITIAL TOPICS
    # CREATE A TOPIC FROM GANDHI JSON
    # CROSS CHECK THAT TOPIC
    # DELETE THE TOPIC
    # CROSS CHECK THAT TOPIC
    pass

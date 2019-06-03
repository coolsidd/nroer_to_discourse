import csv
from tempfile import NamedTemporaryFile
import shutil
import ast


def append_data(nid, did, filename, **kwargs):
    with open(filename, "r+") as readFile:
        reader = csv.reader(readFile)
        writer = csv.writer(readFile)
        lines = list(reader)
        i = 0
        for row in lines:
            if row[0] == [nid] or row[1] == [did]:
                print("failure")
                raise AssertionError
        writer.writerows([[nid, did, kwargs]])


def identify(name, value, filename):
    with open(filename, "r") as readFile:
        reader = csv.reader(readFile)
        name_found = False
        for row in reader:
            if row[0] == name and row[1] == value:
                row[-1] = ast.literal_eval(row[-1])
                return row
            if row[0] == name:
                name_found = True
    if name_found:
        return None
    else:
        return None

def store(name, value, data, filename):
    temp_file = NamedTemporaryFile(mode="w", delete=False)
    with open(filename, "r+") as csv_file:
        reader = csv.reader(csv_file)
        writer = csv.writer(temp_file)
        changed = False
        for row in reader:
            if row[0] == name and row[1] == value:
                row[2] = ast.literal_eval(row[2])
                row[2] = row[2] + data
                changed = True
            writer.writerow(row)
        if not changed:
            print("Addding data")
            writer.writerow([name, value, data])
        temp_file.flush()
        csv_file.flush()
        shutil.move(temp_file.name, filename)
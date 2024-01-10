import csv
from readrides import RideData

def read_csv_as_dicts(filename, col_types):

    records = []
    with open(filename, "r") as f:
        rows = csv.reader(f)
        header = next(rows)

        for row in rows:
            records.append({name: func(val) for name, func, val in zip(header, col_types, row)})
    return records

def read_csv_as_columns(filename, col_types):

    records = RideData()
    with open(filename, "r") as f:
        rows = csv.reader(f)
        header = next(rows)

        for row in rows:
            records.append({name: func(val) for name, func, val in zip(header, col_types, row)})
    return records
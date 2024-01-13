import csv
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def read_csv_as_dicts(filename: str, types: list, *, headers=None) -> list:
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    '''
    with open(filename) as file:
        return csv_as_dicts(file, types, headers=headers)

def read_csv_as_instances(filename: str, cls) -> list:
    '''
    Read CSV data into a list of instances
    '''
    with open(filename) as file:
        return csv_as_instances(file, cls, headers=headers)

def convert_csv(lines, create_record, *, headers=None):
    '''

    '''
    records = []
    rows = csv.reader(lines)

    if headers is None:
        headers = next(rows)
    for idx, row in enumerate(rows):
        try:
            record = create_record(headers, row)
            records.append(record)
        except ValueError as e:
            log.warning(f"Row {idx+1}: Bad row {row}")
            log.debug(f"Row {idx+1}: Reason: {e}")
    return records

def csv_as_dicts(file, types, *, headers=None) -> list:
    '''

    '''
    return convert_csv(file, 
                       lambda headers, row: { name: func(val) for name, func, val in zip(headers, types, row) })

def csv_as_instances(file, cls, *, headers=None) -> list:
    '''
    '''
    return convert_csv(file,
                       lambda headers, row: cls.from_row(row))    
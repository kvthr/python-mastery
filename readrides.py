from collections import namedtuple, abc
import csv

class RideData(abc.Sequence):
    def __init__(self):
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # Assume all have the same length
        return len(self.routes)

    def __getitem__(self, i):

        if type(i) is slice:
            return [{
            'route': self.routes[i],
            'date': self.dates[i],
            'daytype': self.daytypes[i],
            'rides': self.numrides[i]
        } for i in range(*i.indices(len(self)))]
        return {
            'route': self.routes[i],
            'date': self.dates[i],
            'daytype': self.daytypes[i],
            'rides': self.numrides[i]
        }

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])

def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records

def read_rides_as_columns(filename):
    '''
    Read the bus ride data into 4 lists, representing columns
    '''
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)

def read_rides_as_dictionaries(filename):
    '''
    Read the bus ride data as a list of dictionaries
    '''
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        for row in rows:
            records.append({
                'route': row[0],
                'date': row[1],
                'daytype': row[2],
                'rides': int(row[3]),
            })
    return records

class Row():
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides
    
    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1], row[2], int(row[3]))

def read_rides_as_classes(filename):
    '''
    Read the bus ride data as a list of dictionaries
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        for row in rows:
            row_ = Row(
                route=row[0],
                date=row[1],
                daytype=row[2],
                rides=int(row[3])
            )
            records.append(row_)
            
    return records

RowNT = namedtuple('RowNT', ['route', 'date', 'daytype', 'rides'])
def read_rides_as_namedtuples(filename):
    '''
    Read the bus ride data as a list of dictionaries
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        for row in rows:
            row_ = RowNT(row[0], row[1], row[2], row[3])
            records.append(row_)     
            
    return records


if __name__ == '__main__':
    import tracemalloc
    tracemalloc.start()
    rows = read_rides_as_classes('Data/ctabus.csv')
    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
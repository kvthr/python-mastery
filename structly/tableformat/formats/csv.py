from ..tableformat import TableFormatter

class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(','.join(h for h in headers))

    def row(self, rowdata):
        print(','.join(str(d) for d in rowdata))

from ..tableformat import TableFormatter

class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print("<tr> ", end="")
        print(' '.join(f"<th>{h}</th>" for h in headers), end="")
        print(" </tr>")

    def row(self, rowdata):
        print("<tr> ", end="")
        print(' '.join(f"<td>{str(d)}</td>" for d in rowdata), end="")
        print(" </tr>")

import csv
import os
import json
from enum import Enum

csv.register_dialect('pipe', delimiter='|', quoting=csv.QUOTE_MINIMAL)
csv.register_dialect('comma', delimiter=',', quoting=csv.QUOTE_MINIMAL)
csv.register_dialect('semicolon', delimiter=';', quoting=csv.QUOTE_MINIMAL)

# Used as delimiter types for input file
class InputDelim(Enum):
    COMMA = 'comma'
    PIPE = 'pipe'
    SEMICOLON = 'semicolon'

class CSVHandler:
    def __init__(self,csv_file,delim=InputDelim.COMMA):
        self._csv_file = csv_file
        self._delim = delim        
        self._read_csv()

    def _read_csv(self):
        # print("Reading  : {}".format(self._csv_file))
        # print("Delimiter: '{}'".format(self._delim))
        with open(self._csv_file, newline='') as csvfile_read:
            csv_data = csv.DictReader(csvfile_read, dialect=self._delim.value)
            self._headers = csv_data.fieldnames
            self._rows = [row for row in csv_data]

    def headers(self):
        return self._headers

    def rows(self):
        return self._rows

    def print_csv(self,pretty=False):
        if pretty is True:
            print(json.dumps(self.rows(),indent=4))
        else:
            print(json.dumps(self.rows()))

    def _columns_exist(self,cols):
        # Verify proper column being updated
        return set(cols).issubset(set(self._headers))

    def update_row(self,row_num,cols):
        if self._columns_exist([*cols]) == True:
            self._rows[row_num].update(cols)
        else:
            print("One of the following columns does NOT exist: ", ", ".join(cols.keys()))

    def _filter_csv(self,filters):
        for fltr in filters:
            self.csv = list(filter(fltr,self.csv))
        return self.csv

    # Allows for passing of a callable function to update rows
    def update_rows(self,**cols):
        for i,row in enumerate(self._rows):
            for col,value in cols.items():
                updated_col = {col: value(row) if callable(value) else value}
                self.update_row(i,updated_col)

    def write_csv(self, outputFile=None):
        if outputFile is None:
            outputFile = self._csv_file + ".modified"

        with open(outputFile,"w") as csvfile_write:
            csv_writer = csv.DictWriter(csvfile_write, fieldnames=self._headers, dialect=self._delim.value)
            csv_writer.writeheader()
            csv_writer.writerows(self._rows)

# For testing
if __name__ == '__main__':
    csvhandler = CSVHandler('samples/sample-input.csv')
    csvhandler.print_csv()

    print(csvhandler.headers())
    print(csvhandler.rows())
    csvhandler.update_row(1,{"dob":"01-01-2011"
                            ,"gender":"F"})
    print(csvhandler.rows())

    csv_updates = {
        "dob": lambda row : ("02-02-2022" if row['dob'] is None or row['gender'] == "F" else row['dob'])
    }
    csvhandler.update_rows(**csv_updates)
    print(csvhandler.rows())
    csvhandler.print_csv(pretty=True)
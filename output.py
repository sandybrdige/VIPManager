
import sqlite3

import csv, codecs,io

class UnicodeWriter:


    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):

        self.queue = io.StringIO()

        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)

        self.stream = f

        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):

        self.writer.writerow(row)

        data = self.queue.getvalue()


        data = self.encoder.encode(data)

        self.stream.write(data)


        self.queue.truncate(0)
        self.queue.seek(0)

    def writerows(self, rows):

        for row in rows:

            self.writerow(row)
if __name__=="__main__":
    # conn = sqlite3.connect('VIPdatabase.db')
    #

    a=(0.8)
    b=(494899)
    c=float(a)*float(b)
    print(round(c,1))
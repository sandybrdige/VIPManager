import sqlite3
import time

from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtSql import *

import sys

db = QSqlDatabase.addDatabase("QSQLITE")

db.setDatabaseName('./a.db')

if db.open():
    print
    "db is open"


class FF(QDialog):

    def __init__(self, parent=None):
        super(FF, self).__init__(parent)

        self.resize(300, 300)

        self.model = QSqlTableModel(self)

        self.model.setTable("user")

        self.model.setHeaderData(0, Qt.Horizontal, QVariant("xuhao"))

        self.model.setHeaderData(1, Qt.Horizontal, QVariant("content"))

        self.model.select()

        self.view = QTableView(self)

        self.view.resize(300, 300)

        self.view.setModel(self.model)

        self.view.resizeColumnsToContents()

        # 基类是qmainwindow是用这个方法添加

        # self.setCentralWidget(self.view)

        query = QSqlQuery()

        query.exec_("select * from user")

        if query.next():
            print
            query.value(1).toString()


app = QApplication(sys.argv)

f = FF()

f.show()

app.exec_()

if __name__=="__main__":

    conn = sqlite3.connect('VIPdatabase.db')
    c = conn.cursor()
    # c.execute('''CREATE TABLE VIPinfo
    #        (ID integer PRIMARY KEY autoincrement     NOT NULL,
    #        NAME           TEXT    NOT NULL,
    #        VIPID            INT     NOT NULL,
    #        PHONE         INT     NOT NULL,
    #        TOTALCOST         REAL     NOT NULL,
    #        VIPlv         TEXT     NOT NULL,
    #        VIPpoint      REAL     NOT NULL,
    #        DISCOUNT      REAL     NOT NULL
    #        );''')
    ID='103'
    # c.execute(('UPDATE VIPinfo SET VIPlV=CASE '
    #            'WHEN (VIPPOINT BETWEEN 0 AND 200) THEN "SILVER" '
    #            'WHEN (VIPPOINT BETWEEN 201 AND 500) THEN "GOLD" '
    #            'WHEN (VIPPOINT BETWEEN 501 AND 1000) THEN "DIAMOND" '
    #            'WHEN (VIPPOINT>=1000) THEN "CROWN" '
    #            'ELSE VIPLV END, '
    #            'DISCOUNT=CASE WHEN (VIPPOINT BETWEEN 0 AND 200) THEN 1 '
    #            'WHEN (VIPPOINT BETWEEN 201 AND 500) THEN 0.9 '
    #            'WHEN (VIPPOINT BETWEEN 501 AND 1000) THEN 0.8 '
    #            'WHEN (VIPPOINT>1000) THEN 0.75 '
    #            'ELSE DISCOUNT END WHERE VIPID=%s') % (ID))
    # cursor=c.execute(('SELECT SUM(COST) FROM CostDetail WHERE VIPID=%s')%(ID))
    # value=cursor.fetchone()
    # print(value)
    # conn.commit()
    # conn.close()
    # print("这是What")
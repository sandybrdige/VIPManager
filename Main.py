# -*- coding: utf-8 -*-
from PyQt5 import QtCore,QtGui
import sys
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow,QItemDelegate,QHeaderView,QTableView,QDialog,QLineEdit
from PyQt5.QtSql import QSqlTableModel,QSqlDatabase
from VIPManager import Ui_MainWindow
import sqlite3
import time
from PyQt5 import sip
import csv,io,codecs
from Dialog import Ui_Dialog

class Manager(QMainWindow,Ui_MainWindow):


    def __init__(self):
        super(Manager, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.addNewVip)
        self.pushButton_2.clicked.connect(self.cancelQuery)
        self.pushButton_3.clicked.connect(self.QueryVipDetail)
        self.pushButton_4.clicked.connect(self.QueryVip)
        self.pushButton_5.clicked.connect(self.CleanAll)
        self.lineEdit.returnPressed.connect(self.selectVIPthID)
        self.lineEdit_4.returnPressed.connect(self.addNewVip)
        self.lineEdit_3.returnPressed.connect(self.selectVIPthPhone)
        self.actionOutput_CostDetails.triggered.connect(self.CreateCsv)
        self.actionOutput_VIPinfo.triggered.connect(self.GenerateCsv)
        self.lineEdit_5.returnPressed.connect(self.selectVIPthID5)
        self.lineEdit_7.returnPressed.connect(self.selectVIPthPhone7)
        self.flag="disable"
        self.actionEnable.triggered.connect(self.enableedit)
        self.actionDiable.triggered.connect(self.disableedit)

    def enableedit(self):
        my=MyDialog()
        my.flagpipe.connect(self.change)
        my.exec()
        return

    def change(self,msg):
        self.flag=msg
        print(self.flag)

    def disableedit(self):
        self.flag="disable"
        return
    def addNewVip(self):
        ID=self.lineEdit.text()
        NAME=self.lineEdit_2.text()
        PHONE=self.lineEdit_3.text()
        CONSUME=self.lineEdit_4.text()
        mes=[ID,NAME,PHONE,CONSUME]
        try:
            self.thread=DataBase(mes)
            self.thread.sig.connect(self.callback)
            self.thread.handlevip()
        except:
            pass
    def CreateCsv(self):
        try:
            self.write=DataBase()
            self.write.CreatCSVdetail()
        except:
            pass
    def GenerateCsv(self):
        try:
            self.write=DataBase()
            self.write.CreatCSVVIP()
        except:
            pass
    def selectVIPthID(self):
        ID=self.lineEdit.text()
        mes=[ID,]
        try:
            self.seth=DataBase(mes)
            self.seth.sig.connect(self.selectvipcallback)
            self.seth.selectVIPthid()
        except:
            raise
    def selectVIPthID5(self):
        ID=self.lineEdit_5.text()
        mes=[ID,]
        try:
            self.seth=DataBase(mes)
            self.seth.sig.connect(self.selectvipcallback5)
            self.seth.selectVIPthid()
        except:
            raise
    def selectvipcallback(self,msg):
        self.lineEdit_3.setText(str(msg[0]))
        self.lineEdit_2.setText(str(msg[1]))
    def selectvipcallback5(self,msg):
        self.lineEdit_6.setText(str(msg[1]))
        self.lineEdit_7.setText(str(msg[0]))
    def selectVIPthPhone(self):
        PHONE=self.lineEdit_3.text()
        mes=[PHONE,]
        try:
            self.sethp=DataBase(mes)
            self.sethp.sig.connect(self.selectphonecallback)
            self.sethp.selectVIPthphone()
        except:
            raise
    def selectVIPthPhone7(self):
        PHONE=self.lineEdit_7.text()
        mes=[PHONE,]
        try:
            self.sethp=DataBase(mes)
            self.sethp.sig.connect(self.selectphonecallback7)
            self.sethp.selectVIPthphone()
        except:
            raise
    def selectphonecallback(self,msg):


        self.lineEdit.setText(str(msg[1]))
        self.lineEdit_2.setText(str(msg[0]))
    def selectphonecallback7(self,msg):


        self.lineEdit_5.setText(str(msg[1]))
        self.lineEdit_6.setText(str(msg[0]))
    def callback(self,msg):
        if len(msg)==5:
            self.lineEdit_8.setText(str(msg[0]))
            self.lineEdit_9.setText(str(msg[1]))
            self.lineEdit_10.setText(str(msg[2]))
            self.lineEdit_11.setText(str(msg[3]))
            self.lineEdit_12.setText(str(msg[4]))
        else:
            self.lineEdit_9.setText(str(msg[0]))
    def cancelQuery(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()
        self.lineEdit_11.clear()
        self.lineEdit_12.clear()
    def QueryVipDetail(self):
        queryid=[self.lineEdit_5.text(),]
        try:
            self.set = DataBase(queryid)
            self.set.model.connect(self.QueryVipDetailcallback)
            self.set.QueryVipDetail()
        except:
            raise
    def QueryVipDetailcallback(self,model):
        self.tableView.setModel(model)
        #self.tableView.setItemDelegateForColumn(0, EmptyDelegate(self))
        self.tableView.horizontalHeader().setStretchLastSection(True)
        if self.flag == "enable":
            self.tableView.setEditTriggers(QTableView.DoubleClicked)
            self.tableView.setItemDelegateForColumn(0, EmptyDelegate(self))
        if self.flag == "disable":
            self.tableView.setEditTriggers(QTableView.NoEditTriggers)


    def QueryVip(self):
        queryid=[self.lineEdit_5.text(),]
        try:
            self.set = DataBase(queryid)
            self.set.model.connect(self.QueryVipcallback)
            self.set.QueryVip()
        except:
            raise
    def QueryVipcallback(self,model):
        if self.flag=="enable":
            self.tableView.setEditTriggers(QTableView.DoubleClicked)
            self.tableView.setItemDelegateForColumn(0, EmptyDelegate(self))
        if self.flag=="disable":
            self.tableView.setEditTriggers(QTableView.NoEditTriggers)
        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

    def CleanAll(self):
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        empty=None
        self.tableView.setModel(empty)

class MyDialog(QDialog,Ui_Dialog):
    flagpipe=pyqtSignal(str)

    def __init__(self, parent = None):
        print("启动")
        super(MyDialog, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.verifypw)
        self.pushButton_2.clicked.connect(self.cl)
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.lineEdit.returnPressed.connect(self.verifypw)
        self.pw="123456"
        self.flag="enable"

    def cl(self):
        print("关闭对话")
        self.close()

    def verifypw(self):
        print("开始校验")
        if self.lineEdit.text()==self.pw:
            print("密码验证正确")
            self.flagpipe.emit(self.flag)
            self.close()
        else:
            print("密码验证错误")
            self.label_3.setText("密码输入错误")

        return




class EmptyDelegate(QItemDelegate):

    def __init__(self, parent):
        super(EmptyDelegate, self).__init__(parent)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class DataBase(QtCore.QThread):
    sig=pyqtSignal(list)
    model=pyqtSignal(QSqlTableModel)


    def __init__(self,message=None):
        super(DataBase, self).__init__()
        self.message=message
        self.database=sqlite3.connect('VIPdatabase.db')

    def handlevip(self):
        TIME = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
        conn = self.database
        c = conn.cursor()
        ID = self.message[0]
        NAME = self.message[1]
        PHONE = self.message[2]
        CONSUME = self.message[3]
        try:
            judge = c.execute("SELECT * from VIPinfo where VIPID=%s" % (ID))
            value = judge.fetchall()
            if value == list():
                c.execute("INSERT INTO VIPinfo VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s')" % (
                NAME, ID, PHONE, CONSUME, "SILVER", CONSUME, "1"))
                c.execute(('UPDATE VIPinfo SET VIPlV=CASE '
                           'WHEN (VIPPOINT BETWEEN 0 AND 499) THEN "SILVER" '
                           'WHEN (VIPPOINT BETWEEN 500 AND 999) THEN "GOLD" '
                           'WHEN (VIPPOINT BETWEEN 1000 AND 1999) THEN "PLATINUM" '
                           'WHEN (VIPPOINT>=2000) THEN "DIAMOND" '
                           'ELSE VIPLV END, '
                           'DISCOUNT=CASE WHEN (VIPPOINT BETWEEN 0 AND 499) THEN 1 '
                           'WHEN (VIPPOINT BETWEEN 500 AND 999) THEN 0.9 '
                           'WHEN (VIPPOINT BETWEEN 1000 AND 1999) THEN 0.85 '
                           'WHEN (VIPPOINT>=2000) THEN 0.8 '
                           'ELSE DISCOUNT END WHERE VIPID=%s') % (ID))
                judge = c.execute("SELECT * from VIPinfo where VIPID=%s" % (ID))
                value = judge.fetchone()
                VIPID = value[2]
                VIPLV = value[5]  # 会员等级
                VIPPoint = round(value[6],2)  # VIP点数
                VIPDiscount = value[7]
                VIPprize = round(float(VIPDiscount) * float(CONSUME),2)
                mes = [VIPID, VIPPoint, VIPLV, VIPDiscount, VIPprize]
                c.execute(
                    "INSERT INTO CostDetail VALUES(NULL,'%s','%s','%s','%s','%s')" % (NAME, ID, PHONE, VIPprize, TIME))
                self.sig.emit(mes)



            else:
                c.execute(
                    "UPDATE VIPinfo SET TOTALCOST=(SELECT SUM(COST) FROM CostDetail WHERE VIPID=%s),VIPPOINT=(SELECT SUM(COST) FROM CostDetail WHERE VIPID=%s) WHERE VIPID=%s" % (
                    ID,ID,ID))
                c.execute(('UPDATE VIPinfo SET VIPlV=CASE '
                           'WHEN (VIPPOINT BETWEEN 0 AND 499) THEN "SILVER" '
                           'WHEN (VIPPOINT BETWEEN 500 AND 999) THEN "GOLD" '
                           'WHEN (VIPPOINT BETWEEN 999 AND 1999) THEN "PLATINUM" '
                           'WHEN (VIPPOINT>=2000) THEN "DIAMOND" '
                           'ELSE VIPLV END, '
                           'DISCOUNT=CASE WHEN (VIPPOINT BETWEEN 0 AND 499) THEN 1 '
                           'WHEN (VIPPOINT BETWEEN 500 AND 999) THEN 0.9 '
                           'WHEN (VIPPOINT BETWEEN 999 AND 1999) THEN 0.85 '
                           'WHEN (VIPPOINT>=2000 THEN 0.8 '
                           'ELSE DISCOUNT END WHERE VIPID=%s') % (ID))
                judge = c.execute("SELECT * from VIPinfo where VIPID=%s" % (ID))
                value = judge.fetchone()
                VIPID=value[2]
                VIPLV=value[5]#会员等级
                VIPPoint=round(value[6],2)#VIP点数
                VIPDiscount=value[7]
                VIPprize=round(float(VIPDiscount) * float(CONSUME),2)
                remes=[VIPID,VIPPoint,VIPLV,VIPDiscount,VIPprize]
                c.execute(
                    "INSERT INTO CostDetail VALUES(NULL,'%s','%s','%s','%s','%s')" % (NAME, ID, PHONE, VIPprize, TIME))
                self.sig.emit(remes)

            conn.commit()
            conn.close()

        except:
            conn.rollback()
            conn.close()
            print('数据库操作错误')
            #self.sig.emit(message)
            raise

    def selectVIPthid(self):
        conn = self.database
        c = conn.cursor()
        ID=self.message[0]
        try:
            judge = c.execute("SELECT NAME,PHONE from VIPinfo where VIPID=%s" % (ID))
            value=judge.fetchall()
            NAME=value[0][1]
            PHONE = value[0][0]
            mesg = [NAME, PHONE]
            self.sig.emit(mesg)
        except:
            conn.close()

    def selectVIPthphone(self):
        conn = self.database
        c = conn.cursor()
        PHONE=self.message[0]
        try:
            judge = c.execute("SELECT VIPID,NAME from VIPinfo where PHONE=%s" % (PHONE))
            value=judge.fetchall()
            VIPID=value[0][1]
            NAME = value[0][0]
            mesg = [VIPID, NAME]
            self.sig.emit(mesg)
        except:
            conn.close()


    def CreatCSVdetail(self):
        conn = self.database
        c = conn.cursor()
        c.execute('select * from CostDetail')
        filename='COSTDETAIL.csv'
        with open(filename, 'w', encoding='utf-8',newline='') as f:
            csv_wrtie = csv.writer(f, dialect=csv.excel)
            csv_wrtie.writerow(('KEY', 'NAME','ID','PHONE','COST','COSTTIME'))
        writer = UnicodeWriter(open(filename, "ab"))
        writer.writerows(c)

    def CreatCSVVIP(self):
        conn = self.database
        c = conn.cursor()
        c.execute('select * from VIPinfo')
        filename = 'VIPINFO.csv'
        with open(filename, 'w', encoding='utf-8',newline='') as f:
            csv_wrtie = csv.writer(f, dialect=csv.excel)
            csv_wrtie.writerow(('KEY', 'NAME','ID','PHONE','VIPPOINT','VIPLV','TOTALCOST','DISCOUNT'))
        writer = UnicodeWriter(open(filename, "ab"))
        writer.writerows(c)

    def QueryVipDetail(self):
        ID=self.message[0]
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName("VIPdatabase.db")
        db.open()
        model = QSqlTableModel()
        model.setTable("CostDetail")
        model.setFilter("VIPID="+ID)
        model.select()
        model.setSort(0, Qt.AscendingOrder)
        model.setHeaderData(0, Qt.Horizontal, "Key")
        model.setHeaderData(1, Qt.Horizontal, "Custom_Name")
        model.setHeaderData(2, Qt.Horizontal, "ID")
        model.setHeaderData(3, Qt.Horizontal, "Phone")
        model.setHeaderData(4, Qt.Horizontal, "Cost_Money")
        model.setHeaderData(5, Qt.Horizontal, "Cost_Date")
        self.model.emit(model)

    def QueryVip(self):
        ID=self.message[0]
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName("VIPdatabase.db")
        db.open()
        model = QSqlTableModel()
        model.setTable("VIPinfo")
        model.setFilter("VIPID="+ID)
        model.select()
        model.setSort(0, Qt.AscendingOrder)
        model.setHeaderData(0, Qt.Horizontal, "Key")
        model.setHeaderData(1, Qt.Horizontal, "Custom_Name")
        model.setHeaderData(2, Qt.Horizontal, "ID")
        model.setHeaderData(3, Qt.Horizontal, "Phone")
        model.setHeaderData(4, Qt.Horizontal, "Total_Cost_Money")
        model.setHeaderData(5, Qt.Horizontal, "VIP_Level")
        model.setHeaderData(6, Qt.Horizontal, "VIP_Point")
        model.setHeaderData(7, Qt.Horizontal, "VIP_Discount")
        self.model.emit(model)






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
    app = QApplication(sys.argv)
    M = Manager()
    M.show()
    sys.exit(app.exec_())

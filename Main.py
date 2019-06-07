# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QLabel,QMessageBox
from VIPManager import Ui_MainWindow
import sqlite3
import time
from PyQt5 import sip
import csv,io,codecs


class Manager(QMainWindow,Ui_MainWindow):


    def __init__(self):
        super(Manager, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.addNewVip)
        self.pushButton_2.clicked.connect(self.cancelQuery)
        self.pushButton_3.clicked.connect(self.QueryVipDetail)
        self.lineEdit.returnPressed.connect(self.selectVIPthID)
        self.lineEdit_4.returnPressed.connect(self.addNewVip)
        self.lineEdit_3.returnPressed.connect(self.selectVIPthPhone)
        self.actionOutput_CostDetails.triggered.connect(self.CreateCsv)
        self.actionOutput_VIPinfo.triggered.connect(self.GenerateCsv)



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

    def selectvipcallback(self,msg):
        self.lineEdit_3.setText(str(msg[0]))
        self.lineEdit_2.setText(str(msg[1]))

    def selectVIPthPhone(self):
        PHONE=self.lineEdit_3.text()
        mes=[PHONE,]
        print(mes)
        try:
            self.sethp=DataBase(mes)
            self.sethp.sig.connect(self.selectphonecallback)
            self.sethp.selectVIPthphone()
        except:
            raise

    def selectphonecallback(self,msg):


        self.lineEdit.setText(str(msg[1]))
        self.lineEdit_2.setText(str(msg[0]))






    def callback(self,msg):
        if len(msg)==5:
            print("测试回调：",msg,msg[0],msg[1],msg[2],msg[3])
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

    def QueryVipDetail(self):
        print("Hasaki")
        queryid=self.lineEdit_5.text()
        queryname=self.lineEdit_6.text()
        queryphone=self.lineEdit_7.text()
        print(queryid,queryname,queryphone)


class DataBase(QtCore.QThread):
    sig=pyqtSignal(list)


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
        print(PHONE)
        CONSUME = self.message[3]
        try:
            judge = c.execute("SELECT * from VIPinfo where VIPID=%s" % (ID))
            value = judge.fetchall()
            if value == list():
                print("开始增加新会员")
                c.execute("INSERT INTO VIPinfo VALUES(NULL,'%s','%s','%s','%s','%s','%s','%s')" % (
                NAME, ID, PHONE, CONSUME, "SILVER", CONSUME, "1"))
                c.execute(('UPDATE VIPinfo SET VIPlV=CASE '
                           'WHEN (VIPPOINT BETWEEN 0 AND 200) THEN "SILVER" '
                           'WHEN (VIPPOINT BETWEEN 201 AND 500) THEN "GOLD" '
                           'WHEN (VIPPOINT BETWEEN 501 AND 1000) THEN "DIAMOND" '
                           'WHEN (VIPPOINT>=1000) THEN "CROWN" '
                           'ELSE VIPLV END, '
                           'DISCOUNT=CASE WHEN (VIPPOINT BETWEEN 0 AND 200) THEN 1 '
                           'WHEN (VIPPOINT BETWEEN 201 AND 500) THEN 0.9 '
                           'WHEN (VIPPOINT BETWEEN 501 AND 1000) THEN 0.8 '
                           'WHEN (VIPPOINT>1000) THEN 0.75 '
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
                print("新增回调信息发出，", mes)
                self.sig.emit(mes)



            else:
                c.execute(
                    "UPDATE VIPinfo SET TOTALCOST=(SELECT SUM(COST) FROM CostDetail WHERE VIPID=%s),VIPPOINT=(SELECT SUM(COST) FROM CostDetail WHERE VIPID=%s) WHERE VIPID=%s" % (
                    ID,ID,ID))
                c.execute(('UPDATE VIPinfo SET VIPlV=CASE '
                           'WHEN (VIPPOINT BETWEEN 0 AND 200) THEN "SILVER" '
                           'WHEN (VIPPOINT BETWEEN 201 AND 500) THEN "GOLD" '
                           'WHEN (VIPPOINT BETWEEN 501 AND 1000) THEN "DIAMOND" '
                           'WHEN (VIPPOINT>=1000) THEN "CROWN" '
                           'ELSE VIPLV END, '
                           'DISCOUNT=CASE WHEN (VIPPOINT BETWEEN 0 AND 200) THEN 1 '
                           'WHEN (VIPPOINT BETWEEN 201 AND 500) THEN 0.9 '
                           'WHEN (VIPPOINT BETWEEN 501 AND 1000) THEN 0.8 '
                           'WHEN (VIPPOINT>1000) THEN 0.75 '
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
                print("回调信息发出，", remes)
                self.sig.emit(remes)

            conn.commit()
            conn.close()

        except:
            #message=["数据库操作出错，请稍后重试",]
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
        print(PHONE)
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

import sqlite3
import time


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
    cursor=c.execute(('SELECT SUM(COST) FROM CostDetail WHERE VIPID=%s')%(ID))
    value=cursor.fetchone()
    print(value)
    conn.commit()
    conn.close()
    print("这是What")
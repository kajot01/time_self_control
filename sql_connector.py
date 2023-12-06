import mysql.connector
from datetime import date
import sys
import os


def start_sql_connection():

    MARIADBIP = os.getenv("MARIADBIP")

    if MARIADBIP == "":
        print("Blad: brak zmiennej MARIADBIP")
        sys.exit(1)

    print(f"Serwer bazy danych {MARIADBIP}")
    return MARIADBIP


class SQLConn:

    def __init__(self, port, user, passwd, db):
        self.MARIADBIP = start_sql_connection()
        self.conn = mysql.connector.connect(host=self.MARIADBIP, port=port, user=user, passwd=passwd, db=db)

    def make_date_record(self, d, t_start, t_stop, is_productive, duration):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT EXISTS(SELECT * from days WHERE day=DATE(%s));",
                    params=(d,))
        if not cur.fetchone():
            cur.execute("INSERT INTO days (day) VALUES (%s);", params=(d,))

        d_id = self.get_date_id(d)
        print()
        cur.execute("INSERT INTO times VALUES (%s,%s,%s,%s,%s)",
                    params=(d_id, is_productive, t_start, t_stop, duration))

        cur.close()



    # def make_time_record(self):


    def get_date_id(self, f_date):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id FROM days WHERE day=DATE(%s)", params=(f_date, ))
        d_id = dict(cur.fetchone())
        cur.close()
        return d_id.get("id")


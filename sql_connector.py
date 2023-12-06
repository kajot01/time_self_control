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
        self.init_db()


    def make_date_record(self, d, t_start, t_stop, is_productive, duration):
        cur = self.conn.cursor(dictionary=False)
        cur.execute("SELECT EXISTS(SELECT * from days WHERE day=DATE(%s));",
                    params=(d,))
        print("Czy istnieje: "+str(cur.fetchone()))
        if not cur.fetchone():

            cur.execute("INSERT INTO days (day) VALUES (%s);", params=(d,))
            print("Dodano nowy dzień: " + str(d))

        d_id = self.get_date_id(d)
        print("d_id: "+str(d_id))
        cur.execute("INSERT INTO times VALUES (%s,%s,TIME(%s),TIME(%s),%s)",
                    params=(d_id, is_productive, t_start, t_stop, duration))
        self.conn.commit()
        cur.close()


    # def make_time_record(self):


    def get_date_id(self, f_date):
        cur = self.conn.cursor(dictionary=True)
        command = "SELECT id FROM days WHERE day=DATE(%s);"
        data = ("2023-12-06",)
        cur.execute(command, data)
        d_id = cur.fetchone()
        print("d_id in: "+str(d_id))
        cur.close()
        try:
            num_id = d_id.get("id")
            return num_id
        except:
            print("Panie, mamy problem z tym gównem")

    def init_db(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("USE time_counting;")
        self.conn.start_transaction(isolation_level='READ COMMITTED', readonly=False)
        self.conn.rollback()

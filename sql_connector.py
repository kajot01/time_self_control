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


def translate_time(t):
    return str(t[0]) + ":" + str(t[1])



class SQLConn:

    def __init__(self, port, user, passwd, db):
        self.MARIADBIP = start_sql_connection()
        self.conn = mysql.connector.connect(host=self.MARIADBIP, port=port, user=user, passwd=passwd, db=db)
        self.init_db()

    def make_date_record(self, d, is_productive, t_start, t_stop,  duration):
        cur = self.conn.cursor(dictionary=False)
        cur.execute("SELECT EXISTS(SELECT * from days WHERE day=DATE(%s));",
                    params=(d,))

        if cur.fetchone() == (0,):
            cur.execute("INSERT INTO days (day) VALUES (%s);", params=(d,))

        d_id = self.get_date_id(d)
        cur.execute("INSERT INTO times VALUES (%s,%s,TIME(%s),TIME(%s),%s)",
                    params=(d_id, is_productive, translate_time(t_start), translate_time(t_stop), duration))
        self.conn.commit()
        print("Dodano z powodzeniem nowy rekord")
        cur.close()

    def get_date_id(self, f_date):
        cur = self.conn.cursor(dictionary=True)
        command = "SELECT id FROM days WHERE day=DATE(%s);"
        cur.execute(command, (f_date,))
        d_id = cur.fetchone()
        self.conn.commit()
        cur.close()
        try:
            num_id = d_id["id"]
            return num_id
        except:
            print("Panie, mamy problem z tym gównem")

    def init_db(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("USE time_counting;")
        self.conn.start_transaction(isolation_level='READ COMMITTED', readonly=False)
        self.conn.rollback()

    def get_column(self, column, table, td):
        cur = self.conn.cursor(dictionary=True)
        d_id = self.get_date_id(td)
        if d_id is not None:
            command = f"""SELECT {column} FROM {table} WHERE day_id={d_id};"""
            cur.execute(command)
            records = []
            for row in cur.fetchall():
                records.append(str(row[column]))
            self.conn.commit()
            cur.close()
            return records
        else:
            return []

    def get_row_times(self, td):
        d_id = self.get_date_id(td)
        if d_id is not None:
            cur = self.conn.cursor(dictionary=True)
            command = f"""SELECT is_productive, start_time, end_time, duration  
            FROM times
            WHERE day_id={d_id};"""
            cur.execute(command)
            records = []
            for row in cur.fetchall():
                if row["is_productive"]:
                    row["is_productive"] = "Yes"
                else:
                    row["is_productive"] = "No"
                records.append([str(row["start_time"]),
                               str(row["end_time"]), row["duration"], row["is_productive"]])
            self.conn.commit()
            cur.close()

            return records
        else:
            return []


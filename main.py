from tkinter import ttk
from datetime import datetime
from sql_connector import SQLConn


def main():
    con1 = SQLConn(3306, "JML", "cSJH9xB+^SvV", "time_counting")
    con1.make_date_record(datetime.now(), "20:00", "21:00", True, 60)

if __name__ == '__main__':
    main()



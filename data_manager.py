
from sql_connector import SQLConn
from datetime import datetime


def get_time():
    H = int(datetime.now().strftime("%H"))
    m = int(datetime.now().strftime("%M"))
    return [H, m]


def get_date():
    return datetime.now().strftime("%Y-%m-%d")


class DataManager:
    def __init__(self, sql_conn):
        self.sql_conn = sql_conn
        # [Y, m, d]
        self.date = get_date()
        # [H, M]
        self.last_measure = None
        self.is_productive = True
        self.conn = SQLConn(3306, "JML", "cSJH9xB+^SvV", "time_counting")

    def start_timer(self, is_productive):
        if is_productive:
            self.is_productive = True
        else:
            self.is_productive = False

        self.stop_timer()
        self.date = get_date()
        self.last_measure = get_time()

    def stop_timer(self):
        if self.last_measure is not None:
            d = lambda t1, t2: (t2[0] - t1[0]) * 60 + t2[1] - t1[1]
            if self.date == get_date():
                tn = get_time()
                self.sql_conn.make_date_record(self.date, self.is_productive, self.last_measure, tn,
                                               d(self.last_measure, tn))
            else:
                self.sql_conn.make_date_record(self.date, self.is_productive, self.last_measure, "23:59:00",
                                               d(self.last_measure, [23, 59]))
                tn = get_time()
                self.sql_conn.make_date_record(get_date(), self.is_productive, "00:00:00", tn,
                                               d([0, 0], tn))
            self.last_measure = None

    def get_today_records(self):
        # all_is_productive = self.conn.get_column("is_productive", table,  self.date)
        # start_times = self.conn.get_column("start_time", table,  self.date)
        # end_times = self.conn.get_column("end_time", table, self.date)
        # durations = self.conn.get_column("duration", table, self.date)

        get_rows = self.conn.get_row_times(self.date)

        return get_rows

    def get_last_measure(self):
        print("Czas: ",self.translate_time(self.last_measure))
        return self.translate_time(self.last_measure)

    def translate_time(self, t):
        return "{:02d}".format(t[0]) + ":" + "{:02d}".format(t[1])


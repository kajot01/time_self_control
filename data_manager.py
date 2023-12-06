from day_record import DayRecord
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
        self.date = None
        # [H, M]
        self.timer_start = None
        self.is_productive = True
        self.conn = SQLConn(3306, "JML", "cSJH9xB+^SvV", "time_counting")

    def start_timer(self, is_productive):
        if is_productive:
            self.is_productive = True
        else:
            self.is_productive = False

        self.stop_timer()
        self.date = get_date()
        self.timer_start = get_time()

    def stop_timer(self):
        if self.timer_start is not None:
            d = lambda t1, t2: (t2[0] - t1[0]) * 60 + t2[1] - t1[1]
            if self.date == get_date():
                tn = get_time()
                self.sql_conn.make_date_record(self.date, self.is_productive, self.timer_start, tn,
                                               d(self.timer_start, tn))
            else:
                self.sql_conn.make_date_record(self.date, self.is_productive, self.timer_start, "23:59:00",
                                               d(self.timer_start, [23, 59]))
                tn = get_time()
                self.sql_conn.make_date_record(get_date(), self.is_productive, "00:00:00", tn,
                                               d([0, 0], tn))
            self.timer_start = None

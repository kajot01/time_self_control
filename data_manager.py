from day_record import DayRecord
from sql_connector import SQLConn
from datetime import datetime


def get_time():
    return datetime.now()


def get_date():
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    return [year, month, day]

class DataManager:
    def __init__(self, data_b):
        self.data_b = data_b
        # [Y, m, d]
        self.date = 0
        # [H, M]
        self.timer_start = 0
        self.is_productive = True
        self.conn = SQLConn(3306, "JML", "cSJH9xB+^SvV", "time_counting")

    def start_timer(self, is_productive):
        if is_productive:
            self.is_productive = True
        else:
            self.is_productive = False

        self.timer_start = get_time()
        self.date = get_date()

    # def save_entry(self):


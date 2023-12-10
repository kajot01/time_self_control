from sql_connector import SQLConn
from data_manager import DataManager
from gui.main_buttons_widget import MainButtonsWidget
import sys
from PySide6.QtWidgets import QApplication


def main():
    sql_conn = SQLConn(3306, "JML", "cSJH9xB+^SvV", "time_counting")
    dm = DataManager(sql_conn)
    app = QApplication(sys.argv)
    window = MainButtonsWidget(dm)
    window.show()
    app.exec()
    # print(sql_conn.get_row("times", dm.date))


if __name__ == '__main__':
    main()



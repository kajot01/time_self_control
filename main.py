from tkinter import ttk
from datetime import datetime
from sql_connector import SQLConn
from data_manager import DataManager
from main_window import MainWindow
import time
import sys
from PySide6.QtWidgets import QApplication


def main():
    sql_conn = SQLConn(3306, "JML", "cSJH9xB+^SvV", "time_counting")
    dm = DataManager(sql_conn)
    app = QApplication(sys.argv)
    window = MainWindow(dm)
    window.show()
    app.exec()

if __name__ == '__main__':
    main()



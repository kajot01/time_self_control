from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout,\
    QVBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Signal, Slot, Qt
from data_manager import DataManager


def d_status_header():
    r_layout = QHBoxLayout()
    r_layout.addWidget(QLabel("Start"))
    r_layout.addWidget(QLabel("Stop"))
    r_layout.addWidget(QLabel("Duration [min]"))
    r_layout.addWidget(QLabel("Is Productive?"))
    return r_layout


class RecordTable(QWidget):

    def __init__(self, dm: DataManager, rec_num=None):
        super().__init__()
        self.dm = dm
        self.rec_num = rec_num
        self.rec_labels = []
        self.m_layout = self.init_tabel()
        self.setLayout(self.m_layout)

    def init_tabel(self):
        n_layout = QVBoxLayout()
        n_layout.addLayout(d_status_header())
        today_records = self.dm.get_today_records()
        for record in today_records:
            row_layout = QHBoxLayout()
            row_labels = []
            for cell in record:
                l = QLabel(str(cell))
                row_layout.addWidget(l)
                row_labels.append(l)
            self.rec_labels.append(row_labels)
            n_layout.addLayout(row_layout)
        return n_layout

    def update_table(self):
        t_rec = self.dm.get_today_records()
        displayed_row_count = len(self.rec_labels)
        if len(t_rec) > displayed_row_count:
            n_row = QHBoxLayout()
            row_ls = []
            for cell in t_rec[displayed_row_count]:
                l = QLabel(str(cell))
                n_row.addWidget(l)
                row_ls.append(l)
            self.rec_labels.append(row_ls)
            self.m_layout.addLayout(n_row)

    @Slot()
    def update_day_status(self):
        self.update_table()

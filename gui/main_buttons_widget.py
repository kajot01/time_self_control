from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout,\
    QVBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Signal, Slot, Qt
from data_manager import DataManager
from gui.records_widget import RecordTable

class MainButtonsWidget(QWidget):
    def __init__(self, dm: DataManager, parent=None):
        super().__init__(parent)
        self.dm = dm
        self.setWindowTitle("Czas przy elektronice")
        self.setStyleSheet("""
        background-color: #262626;
        color: #FFFFFF;
        font-family: Titillium;
        font-size: 18px;
        """)
        self.r_widget = RecordTable(dm)
        b_layout = self.main_buttons()
        napis = QLabel()
        napis.setText("Ostatnio zmierzony czas:")
        napis.setAlignment(Qt.AlignCenter)

        self.label_czas = QLabel("---")
        main_layout = QGridLayout()
        main_layout.addWidget(napis, 1, 1)
        main_layout.addWidget(self.label_czas, 1, 2)
        main_layout.addLayout(b_layout, 2, 1, 1, 2)
        main_layout.addWidget(self.r_widget, 3, 1, 3, 3)
        self.setLayout(main_layout)

    def main_buttons(self):
        b_start_productive = QPushButton("Start produktywnie")
        b_start_productive.clicked.connect(self.start_prod)
        b_start_productive.clicked.connect(self.r_widget.update_day_status)

        b_start_unproductive = QPushButton("Start bezproduktywnie")
        b_start_unproductive.clicked.connect(self.start_bezprod)
        b_start_unproductive.clicked.connect(self.r_widget.update_day_status)

        b_stop = QPushButton("Stop")
        b_stop.clicked.connect(self.stop_time)
        b_stop.clicked.connect(self.r_widget.update_day_status)

        b_layout = QHBoxLayout()
        b_layout.addWidget(b_start_productive)
        b_layout.addWidget(b_start_unproductive)
        b_layout.addWidget(b_stop)
        return b_layout

    @Slot()
    def start_prod(self):
        self.dm.start_timer(True)
        self.label_czas.setText(self.dm.get_last_measure())
        print("Start prod")

    @Slot()
    def start_bezprod(self):
        self.dm.start_timer(False)
        self.label_czas.setText(self.dm.get_last_measure())
        print("Start bez_prod")

    @Slot()
    def stop_time(self):
        self.dm.stop_timer()
        self.label_czas.setText("---")
        print("Stop")




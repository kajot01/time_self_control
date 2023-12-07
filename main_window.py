from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Signal, Slot, Qt
from data_manager import DataManager


class MainWindow(QWidget):
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
        b_start_productive = QPushButton("Start produktywnie")
        b_start_productive.clicked.connect(self.start_prod)
        b_start_unproductive = QPushButton("Start bezproduktywnie")
        b_start_unproductive.clicked.connect(self.start_bezprod)
        b_stop = QPushButton("Stop")
        b_stop.clicked.connect(self.stop_time)

        napis = QLabel()
        napis.setText("tekst tymczasowy")

        napis.setAlignment(Qt.AlignCenter)
        b_layout = QHBoxLayout()
        b_layout.addWidget(b_start_productive)
        b_layout.addWidget(b_start_unproductive)
        b_layout.addWidget(b_stop)

        main_layout = QGridLayout()
        main_layout.addWidget(napis, 1, 1)
        main_layout.addLayout(b_layout, 2, 1)
        self.setLayout(main_layout)

    @Slot()
    def start_prod(self):
        self.dm.start_timer(True)
        print("Start prod")

    @Slot()
    def start_bezprod(self):
        self.dm.start_timer(False)
        print("Start bez_prod")

    @Slot()
    def stop_time(self):
        self.dm.stop_timer()
        print("Stop")



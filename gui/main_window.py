from PySide6.QtWidgets import QMainWindow
from main_buttons_widget import MainButtonsWidget


class MainWindow(QMainWindow):
    def __init__(self, c_w: MainButtonsWidget):
        super().__init__()
        self.c_w = c_w



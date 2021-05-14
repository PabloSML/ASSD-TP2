from PyQt5.QtWidgets import QDialog
from src.ui.popup import Ui_Dialog


class instrument_selector(QDialog, Ui_Dialog):

    def __init__(self):
        super(instrument_selector, self).__init__()
        self.setupUi(self)






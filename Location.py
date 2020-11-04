from PyQt5 import QtWidgets


class Location(QtWidgets.QListWidgetItem):

    def __init__(self, name):
        super().__init__()
        self.setText(name)
        self.modifiers = []
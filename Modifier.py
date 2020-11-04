from PyQt5 import QtWidgets


class Modifier(QtWidgets.QListWidgetItem):

    def __init__(self):
        super().__init__()
        self.modifier = 1.0
        self.identifier = ""


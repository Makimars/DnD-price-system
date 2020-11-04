from PyQt5 import QtWidgets


class Item(QtWidgets.QListWidgetItem):

    def __init__(self, name):
        super().__init__()
        self.setText(name)
        self.basePrice = 1
        self.groups = []

    def setBasePrice(self, price):
        self.basePrice = price

    def getBasePrice(self):
        return self.basePrice

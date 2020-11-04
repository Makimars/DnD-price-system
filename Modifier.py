from PyQt5 import QtWidgets


class Modifier(QtWidgets.QListWidgetItem):

    def __init__(self):
        super().__init__()
        self.modifier = 1.0
        self.identifier = None

    def loadJson(self, mod, itemList, groups):
        self.modifier = mod["modifier"]
        id = mod["identifier"]
        if type(id) == str:
            self.identifier = id
        else:
            self.identifier = itemList[id]

    def getJson(self, itemList):
        text = "{"

        text += "\"identifier\" : "
        if type(self.identifier) == str:
            text += "\"" + self.identifier + "\""
        else:
            text += str(itemList.index(self.identifier))

        text += ", "

        text += "\"modifier\" : " + str(self.modifier)

        text += " }"
        return text



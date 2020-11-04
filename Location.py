import json
from PyQt5 import QtWidgets
from Modifier import Modifier

class Location(QtWidgets.QListWidgetItem):

    def __init__(self, name):
        super().__init__()
        self.setText(name)
        self.name = name
        self.modifiers = []

    def setText(self, text: str):
        super(Location, self).setText(text)
        self.name = text

    def getModifier(self, name):
        for mod in self.modifiers:
            if mod.identifier.__str__() == name:
                return mod

        return None

    def json(self, itemList):
        json = "{"
        json += "\"name\":\""+ self.name + "\","
        json += "\"modifiers\" : ["

        for mod in self.modifiers:
            if type(mod.identifier) == str:
                json += "\"" + mod.identifier + "\""
            else:
                json += str(itemList.index(mod.identifier)) + ","

        json += "]"
        return json + "}"

    def getModifiersJson(self, itemList):
        json = "["
        comma = False
        for mod in self.modifiers:
            if comma:
                json += " ,"
            json += mod.getJson(itemList)
            comma = True
        json += "]"
        return json

    def loadModifiers(self, text, itemList, groups):
        modifiers = json.loads(text)
        for mod in modifiers:
            newModifier = Modifier()
            newModifier.loadJson(mod, itemList, groups)
            self.modifiers.append(newModifier)

class LocationContainer:
    def __init__(self, name, modifiers):
        self.name = name
        self.modifiers = modifiers
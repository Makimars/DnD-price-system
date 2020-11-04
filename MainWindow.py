import json

from PyQt5 import QtWidgets, QtGui
from Ui_MainWindow import Ui_MainWindow
from Item import Item
from Location import Location, LocationContainer
from Modifier import Modifier

class Container:
    def __init__(self, items, groups, locations):
        self.items = items
        self.groups = groups
        self.locations = locations

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.itemBasePrice.setValidator(QtGui.QDoubleValidator())
        self.ui.modifierEdit.setValidator(QtGui.QDoubleValidator())
        # items
        self.ui.newItem.clicked.connect(self.newItemClicked)
        self.ui.deleteItem.clicked.connect(self.deleteItemClicked)
        self.ui.itemNameEdit.editingFinished.connect(self.saveItem)
        self.ui.itemBasePrice.editingFinished.connect(self.saveItem)
        self.ui.itemGroupSelect.itemSelectionChanged.connect(self.saveItem)
        self.ui.itemEditView.currentItemChanged.connect(self.itemEditViewSelectionChanged)
        self.ui.tabWidget.currentChanged.connect(self.refreshGroupsForItems)
        # groups
        self.ui.groupNameEdit.editingFinished.connect(self.saveGroup)
        self.ui.deleteGroup.clicked.connect(self.deleteGroupClicked)
        self.ui.newGroup.clicked.connect(self.newGroupClicked)
        self.ui.groupEditView.currentItemChanged.connect(self.groupEditViewSelectionChanged)
        # locations
        self.ui.newLocation.clicked.connect(self.newLocation)
        self.ui.deleteLocation.clicked.connect(self.deleteLocation)
        self.ui.locationNameEdit.editingFinished.connect(self.saveLocation)
        self.ui.locationSelection.currentItemChanged.connect(self.locationViewSelectionChanged)
        self.ui.tabWidget.currentChanged.connect(self.refreshModifiersForLocations)
        # modifiers
        self.ui.locationModifierSelection.currentItemChanged.connect(self.refreshModifiers)
        self.ui.locationSelection.currentItemChanged.connect(self.refreshModifiers)
        self.ui.saveModifier.clicked.connect(self.saveModifier)
        self.ui.modifierEdit.editingFinished.connect(self.saveModifier)
        self.ui.modifierTypeSelect.currentIndexChanged.connect(self.refreshModifiersForLocations)
        # Final view
        self.ui.tabWidget.currentChanged.connect(self.refreshFinalLocationsView)
        self.ui.locationsFinalView.currentItemChanged.connect(self.refreshFinalItemsView)
        self.ui.finalItemsView.setColumnCount(2)
        # menubar
        self.ui.actionNew.triggered.connect(self.newFile)
        self.ui.actionOpen.triggered.connect(self.openFile)
        self.ui.actionSave.triggered.connect(self.saveFile)
        # vars
        self.items = []
        self.groups = []
        self.locations = []

    # Items creation

    def newItemClicked(self):
        newItem = Item("NewItem")
        self.items.append(newItem)
        self.ui.itemEditView.addItem(newItem.name)

    def deleteItemClicked(self):
        self.items.pop(self.ui.itemEditView.currentRow())
        self.ui.itemEditView.takeItem(self.ui.itemEditView.currentRow())

    def saveItem(self):
        item = self.items[self.ui.itemEditView.currentRow()]
        if item is None:
            return
        item.name = self.ui.itemNameEdit.text()
        item.basePrice = float(self.ui.itemBasePrice.text())
        self.ui.itemEditView.currentItem().setText(self.ui.itemNameEdit.text())
        # groups
        item.groups.clear()
        items = self.ui.itemGroupSelect.selectedItems()
        for i in range(0, items.__len__()):
            item.groups.append(items[i].text())

    def itemEditViewSelectionChanged(self):
        item = self.items[self.ui.itemEditView.currentRow()]
        self.ui.itemNameEdit.setText(item.name)
        self.ui.itemBasePrice.setText(str(item.basePrice))
        # groups
        self.ui.itemGroupSelect.clearSelection()
        for i in range(0, self.ui.itemGroupSelect.count()):
            group = self.ui.itemGroupSelect.item(i)
            if group.text() in item.groups:
                group.setSelected(True)

    def refreshGroupsForItems(self):
        while self.ui.itemGroupSelect.count() > 0:
            self.ui.itemGroupSelect.takeItem(0)

        for group in self.groups:
            self.ui.itemGroupSelect.addItem(group)

    # Groups management

    def newGroupClicked(self):
        self.groups.append("New Group")
        self.ui.groupEditView.addItem("New Group")

    def deleteGroupClicked(self):
        self.groups.remove(self.ui.groupEditView.currentItem().text())
        self.ui.groupEditView.takeItem(self.ui.groupEditView.currentRow())

    def saveGroup(self):
        if self.ui.groupEditView.currentItem() is None:
            return
        self.ui.groupEditView.currentItem().setText(self.ui.groupNameEdit.text())
        self.groups[self.ui.groupEditView.currentRow()] = self.ui.groupNameEdit.text()

    def groupEditViewSelectionChanged(self, current: QtWidgets.QListWidgetItem):
        self.ui.groupNameEdit.setText(current.text())

    # locations

    def newLocation(self):
        location = Location("New Location")
        self.locations.append(location)
        self.ui.locationSelection.addItem(location)
        self.ui.locationSelection.setCurrentItem(location)

    def deleteLocation(self):
        self.locations.remove(self.ui.locationSelection.currentItem())
        self.ui.locationSelection.takeItem(self.ui.locationSelection.currentRow())

    def saveLocation(self):
        location = self.ui.locationSelection.currentItem()
        if location is None:
            return
        location.setText(self.ui.locationNameEdit.text())

    def locationViewSelectionChanged(self, current: QtWidgets.QListWidgetItem):
        self.ui.locationNameEdit.setText(self.ui.locationSelection.currentItem().text())

    def refreshModifiersForLocations(self):
        while self.ui.locationModifierSelection.count() > 0:
            self.ui.locationModifierSelection.takeItem(0)

        if self.ui.modifierTypeSelect.currentIndex() == 0:
            for group in self.groups:
                self.ui.locationModifierSelection.addItem(group)
                # highlight Groups as gray
                #self.ui.locationModifierSelection.item(self.ui.locationModifierSelection.count()-1).setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
        else:
            for item in self.items:
                self.ui.locationModifierSelection.addItem(item.name)

    # modifiers

    def refreshModifiers(self):
        if self.ui.locationSelection.currentRow() == -1 or self.ui.locationModifierSelection.currentRow() == -1:
            return

        location = self.locations[self.ui.locationSelection.currentRow()]
        modifier = location.getModifier(self.ui.locationModifierSelection.currentItem().text())
        if modifier is not None:
            self.ui.modifierEdit.setText(str(modifier.modifier))
        else:
            self.ui.modifierEdit.setText("1.0")
            modifier = Modifier()
            if self.ui.modifierTypeSelect.currentIndex() == 0:
                modifier.identifier = self.groups[self.ui.locationModifierSelection.currentRow()]
            else:
                modifier.identifier = self.items[self.ui.locationModifierSelection.currentRow()]

            location.modifiers.append(modifier)

    def saveModifier(self):
        if self.ui.locationSelection.currentRow() == -1 or self.ui.locationModifierSelection.currentRow() == -1:
            return

        location = self.locations[self.ui.locationSelection.currentRow()]
        modifier = location.getModifier(self.ui.locationModifierSelection.currentItem().text())
        modifier.modifier = float(self.ui.modifierEdit.text())

    # Final view

    def refreshFinalLocationsView(self):
        while self.ui.locationsFinalView.count() > 0:
            self.ui.locationsFinalView.takeItem(0)

        for location in self.locations:
            self.ui.locationsFinalView.addItem(location.text())

    def refreshFinalItemsView(self):
        self.ui.finalItemsView.clear()
        self.ui.finalItemsView.setRowCount(self.items.__len__())

        for i in range(0, self.items.__len__()):
            self.ui.finalItemsView.setItem(i, 0, QtWidgets.QTableWidgetItem(self.items[i].name))

        location = self.locations[self.ui.locationsFinalView.currentRow()]

        for i in range(0, self.items.__len__()):
            baseModifier = location.getModifier(self.items[i].name)
            if baseModifier is None:
                itemModifier = 1.0
            else:
                itemModifier = baseModifier.modifier

            for group in self.items[i].groups:
                mod = location.getModifier(group)
                if mod is not None:
                    itemModifier *= mod.modifier

            finalPrice = self.items[i].basePrice * itemModifier
            self.ui.finalItemsView.setItem(i, 1, QtWidgets.QTableWidgetItem(str(finalPrice)))

    #munbar

    def newFile(self):
        self.items.clear()
        self.groups.clear()
        self.locations.clear()

    def openFile(self):
        self.newFile()
        print("file: ")
        array = json.loads(input())

        # load items
        for item in array[0]:
            newItem = Item(item["name"])
            newItem.basePrice = item["basePrice"]
            newItem.groups = item["groups"]
            self.items.append(newItem)
            self.ui.itemEditView.addItem(newItem.name)

        # load groups
        for group in array[1]:
            self.groups.append(group)
            self.ui.groupEditView.addItem(group)

        # load locations
        for location in array[2]:
            loc = Location(location["name"])
            loc.loadModifiers(location["modifiers"], self.items, self.groups)
            self.locations.append(loc)
            self.ui.locationSelection.addItem(loc)

    def saveFile(self):
        file = "["

        comma = False
        file += "["
        for item in self.items:
            if comma:
                file += " ,"
            file += json.dumps(item.__dict__)
            comma = True
        file += "],"

        file += json.dumps(self.groups) + ", "

        comma = False
        file += "["
        for location in self.locations:
            if comma:
                file += " ,"
            file += json.dumps(LocationContainer(location.name, location.getModifiersJson(self.items)).__dict__)
            comma = True
        file += "]"

        file += "]"
        print(file)

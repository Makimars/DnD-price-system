from PyQt5 import QtWidgets
from Ui_MainWindow import Ui_MainWindow
from Item import Item
from Location import Location

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # items
        self.ui.newItem.clicked.connect(self.newItemClicked)
        self.ui.deleteItem.clicked.connect(self.deleteItemClicked)
        self.ui.itemNameEdit.editingFinished.connect(self.saveItem)
        self.ui.itemBasePrice.editingFinished.connect(self.saveItem)
        self.ui.itemGroupSelect.currentItemChanged.connect(self.saveItem)
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
        self.ui.modifierEdit.editingFinished.connect(self.saveModifier)
        # vars
        self.items = []
        self.groups = []
        self.locations = []

    # Items creation

    def newItemClicked(self):
        newItem = Item("NewItem")
        self.items.append(newItem)
        self.ui.itemEditView.addItem(newItem)
        #self.ui.itemEditView.setCurrentItem(newItem)

    def deleteItemClicked(self):
        self.items.remove(self.ui.itemEditView.currentItem())
        self.ui.itemEditView.takeItem(self.ui.itemEditView.currentRow())

    def saveItem(self):
        item = self.ui.itemEditView.currentItem()
        if item is None:
            return
        item.setText(self.ui.itemNameEdit.text())
        item.setBasePrice(int(self.ui.itemBasePrice.text()))
        # groups

    def itemEditViewSelectionChanged(self, current: Item):
        self.ui.itemNameEdit.setText(current.text())
        self.ui.itemBasePrice.setText(str(current.getBasePrice()))
        # groups

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

        for group in self.groups:
            self.ui.locationModifierSelection.addItem(group)
        for item in self.items:
            self.ui.locationModifierSelection.addItem(item)

    # modifiers

    def refreshModifiers(self):
        pass

    def saveModifier(self):
        pass

"""      
 #if self.ui.modifierTypeSelect.currentIndex() == 0:
         #   for group in self.groups:
          #      self.ui.locationModifierSelection.addItem(group)
 else:
            for item in self.items:
                self.ui.locationModifierSelection.addItem(item)"""

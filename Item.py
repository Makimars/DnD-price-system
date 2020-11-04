import json

class Item():

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.basePrice = 1
        self.groups = []

    def __str__(self):
        return self.name

    def json(self):
        return {self.name, self.basePrice, self.groups}

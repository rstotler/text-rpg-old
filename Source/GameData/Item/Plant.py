from GameData.Item.Item import Item

class Plant(Item):

    def __init__(self, num):
        Item.__init__(self, num, False)

from dateutil.parser import parse

class Item:

    def __init__(self, id, name, editDatetime, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status
        self.editDatetime = editDatetime

    @classmethod
    def fromTrelloCard(cls, card, list):
        return cls(card['id'], card['name'], parse(card['dateLastActivity']), list['name'])

    def reset(self):
        self.status = 'To Do'

    def start(self):
        self.status = 'Doing'

    def complete(self):
        self.status = 'Done'

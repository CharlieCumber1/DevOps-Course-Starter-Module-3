from dateutil.parser import parse

class Item:

    def __init__(self, id, name, editDatetime, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status
        self.editDatetime = editDatetime

    @classmethod
    def fromMongoDb(cls, object, status):
        return cls(object['_id'], object['name'], object['dateLastActivity'], status)

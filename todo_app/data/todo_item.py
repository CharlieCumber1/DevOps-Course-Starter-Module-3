class Item:
    def __init__(self, id, name, editDatetime, status):
        self.id = id
        self.name = name
        self.status = status
        self.editDatetime = editDatetime

    @classmethod
    def fromMongoDb(cls, object):
        return cls(object['_id'], object['name'], object['dateLastActivity'], object['status'])

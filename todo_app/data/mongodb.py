import os
from todo_app.data.todo_item import Item
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('MONGODB_CONNECTION_STRING'))
        self.db = self.client.get_default_database()
        self.collection = self.db['Tasks']

    def delete_current_database(self):
        self.client.drop_database(self.db)

    def get_items(self):
        return [Item.fromMongoDb(item) for item in self.collection.find()]

    def add_item(self, name):
        now = datetime.utcnow()
        item = {"name": name, "status": "To Do", "dateLastActivity": now}
        self.collection.insert_one(item)
        return

    def start_item(self, id):
        return self.set_item_status(id, "Doing")

    def complete_item(self, id):
        return self.set_item_status(id, "Done")

    def uncomplete_item(self, id):
        return self.set_item_status(id, "To Do")

    def delete_item(self, id):
        self.collection.delete_one({ '_id': ObjectId(id) })
        return
    
    def set_item_status(self, id, status):
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
        return

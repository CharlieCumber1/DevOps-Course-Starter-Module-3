import os
from todo_app.data.todo_item import Item
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from pprint import pprint

class MongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}@cluster0.illz4.mongodb.net/{os.getenv('MONGODB_DATABASE_NAME')}?retryWrites=true&w=majority")
        self.db = self.client.get_default_database()

    def delete_current_database(self):
        self.client.drop_database(self.db)

    def get_collection(self, name):
        return self.db[f'{name}'].find()

    def get_items(self):
        items = []
        for item in self.get_collection("To Do"):
            items.append(Item.fromMongoDb(item, "To Do"))
        for item in self.get_collection("Doing"):
            items.append(Item.fromMongoDb(item, "Doing"))
        for item in self.get_collection("Done"):
            items.append(Item.fromMongoDb(item, "Done"))
        return items

    def get_item(self, id):
        items = self.get_items()
        return next((item for item in items if item.id == ObjectId(id)), None)

    def add_item(self, name):
        now = datetime.utcnow()
        item = {"name": name, "dateLastActivity": now}
        return Item(self.db['To Do'].insert_one(item).inserted_id, name, now)

    def start_item(self, id):
        return self.move_item_to_collection(id, "To Do", "Doing")

    def complete_item(self, id):
        return self.move_item_to_collection(id, "Doing", "Done")

    def uncomplete_item(self, id):
        return self.move_item_to_collection(id, "Done", "To Do")

    def delete_item(self, id):
        item = self.get_item(id)
        self.db[f'{item.status}'].remove({ '_id': item.id })
        return

    def move_item_to_collection(self, id, current_collection, new_collection):
        item = self.db[f'{current_collection}'].find_one_and_delete({"_id": ObjectId(id)})
        item['dateLastActivity'] = datetime.utcnow()
        self.db[f'{new_collection}'].insert_one(item)
        return

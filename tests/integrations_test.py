import pytest
from os import environ
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from todo_app.data.todo_item import Item
from todo_app.user import User
import requests

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app.create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def stub_mongodb():
    return

def stub_get_user(*args, **kwargs):
    return User("test-user")

def stub_get_all_items(self):
    return [
        Item("5f2d2a02e5623c443d7d5190", "Item 1", "2020-08-07T10:16:34.157Z", "To Do"),
        Item("5f2d2a051fe01a43d4a3dc0b", "Item 2", "2020-08-07T10:16:37.040Z", "To Do"),
        Item("5f2d2a0893cdbf6a1d4020bb", "Item 3", "2020-08-07T10:16:40.598Z", "To Do"),
        Item("5f2d2a0d42022d54874e390b", "Item 4", "2020-08-07T10:16:45.924Z", "To Do"),
        Item("5f2d2a2b4ad6605817a8ad7c", "Item 5", "2020-08-07T10:17:15.007Z", "Doing"),
        Item("5f2d2a2e73b9781a72557d06", "Item 6", "2020-08-07T10:17:18.761Z", "Doing"),
        Item("5f2d2a32a2a49e5639fe6eb6", "Item 7", "2020-08-07T10:17:22.185Z", "Doing"),
        Item("5f2d2a388dce853c3ca9f756", "Item 8", "2020-08-07T10:17:28.190Z", "Doing"),
        Item("5f2d2a3ccea4473780f1adea", "Item 9", "2020-08-07T10:17:32.700Z", "Done"),
        Item("5f2d2a3f65144029b6205d3e", "Item 10", "2020-08-07T10:17:35.419Z", "Done"),
        Item("5f2d2a42bc6c370f65f74d64", "Item 11", "2020-08-07T10:17:38.105Z", "Done"),
        Item("5f2d2a450e99c347e8458c7b", "Item 12", "2020-08-07T10:17:41.311Z", "Done")
    ]

def test_index_page(monkeypatch, client):
    monkeypatch.setattr('todo_app.data.mongodb.pymongo.MongoClient', stub_mongodb)
    monkeypatch.setattr('todo_app.data.mongodb.MongoDB.get_items', stub_get_all_items)
    monkeypatch.setattr('flask_login.utils._get_user', stub_get_user)

    response = client.get('/')

    assert 'Item 4' in response.data.decode()
    assert 'Item 5' in response.data.decode()
    assert 'Item 8' in response.data.decode()
    assert 'Item 9' in response.data.decode()
    assert 'Item 12' in response.data.decode()
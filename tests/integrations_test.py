import pytest
from os import environ
from dotenv import load_dotenv, find_dotenv
from todo_app import app
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


@pytest.fixture
def mock_get_request(monkeypatch):

    class MockResponse(object):
        def __init__(self):
            self.status_code = 200
            self.url = 'http://test.com'
            self.headers = {'Something': '1234'}
        
        def json(self):
            return [
                {
                    "id": "mock_list_id_not_started",
                    "name": "To Do",
                    "cards": [
                        {
                            "id": "5f2d2a02e5623c443d7d5190",
                            "dateLastActivity": "2020-08-07T10:16:34.157Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_not_started",
                            "name": "Item 1"
                        },
                        {
                            "id": "5f2d2a051fe01a43d4a3dc0b",
                            "dateLastActivity": "2020-08-07T10:16:37.040Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_not_started",
                            "name": "Item 2"
                        },
                        {
                            "id": "5f2d2a0893cdbf6a1d4020bb",
                            "dateLastActivity": "2020-08-07T10:16:40.598Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_not_started",
                            "name": "Item 3"
                        },
                        {
                            "id": "5f2d2a0d42022d54874e390b",
                            "dateLastActivity": "2020-08-07T10:16:45.924Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_not_started",
                            "name": "Item 4"
                        }
                    ]
                },
                {
                    "id": "mock_list_id_in_progress",
                    "name": "Doing",
                    "cards": [
                        {
                            "id": "5f2d2a2b4ad6605817a8ad7c",
                            "dateLastActivity": "2020-08-07T10:17:15.007Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_in_progress",
                            "name": "Item 5"
                        },
                        {
                            "id": "5f2d2a2e73b9781a72557d06",
                            "dateLastActivity": "2020-08-07T10:17:18.761Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_in_progress",
                            "name": "Item 6"
                        },
                        {
                            "id": "5f2d2a32a2a49e5639fe6eb6",
                            "dateLastActivity": "2020-08-07T10:17:22.185Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_in_progress",
                            "name": "Item 7"
                        },
                        {
                            "id": "5f2d2a388dce853c3ca9f756",
                            "dateLastActivity": "2020-08-07T10:17:28.190Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_in_progress",
                            "name": "Item 8"
                        }
                    ]
                },
                {
                    "id": "mock_list_id_done",
                    "name": "Done",
                    "cards": [
                        {
                            "id": "5f2d2a3ccea4473780f1adea",
                            "dateLastActivity": "2020-08-07T10:17:32.700Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_done",
                            "name": "Item 9"
                        },
                        {
                            "id": "5f2d2a3f65144029b6205d3e",
                            "dateLastActivity": "2020-08-07T10:17:35.419Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_done",
                            "name": "Item 10"
                        },
                        {
                            "id": "5f2d2a42bc6c370f65f74d64",
                            "dateLastActivity": "2020-08-07T10:17:38.105Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_done",
                            "name": "Item 11"
                        },
                        {
                            "id": "5f2d2a450e99c347e8458c7b",
                            "dateLastActivity": "2020-08-07T10:17:41.311Z",
                            "desc": "",
                            "idBoard": "mock_board_id",
                            "idList": "mock_list_id_done",
                            "name": "Item 12"
                        }
                    ]
                }
            ]
    

    def mock_response(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_response)
    
def test_index_page(mock_get_request, client): 
    response = client.get('/')

    assert 'Item 4' in response.data.decode()
    assert 'Item 5' in response.data.decode()
    assert 'Item 8' in response.data.decode()
    assert 'Item 9' in response.data.decode()
    assert 'Item 12' in response.data.decode()
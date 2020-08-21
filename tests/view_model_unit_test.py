import pytest
import todo_app.data.trello_items as trello
from todo_app.view_model import ViewModel
import datetime
from dateutil.parser import parse
from unittest import mock

@pytest.fixture
def test_items():
    test_items = []
    test_items.append(trello.Item.fromTrelloCard({'id': '1',  'name': 'Item 1',  'dateLastActivity': '2020-08-04 10:35:00 UTC'}, {'name': 'To Do'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '2',  'name': 'Item 2',  'dateLastActivity': '2020-08-04 10:35:00 UTC'}, {'name': 'To Do'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '3',  'name': 'Item 3',  'dateLastActivity': '2020-08-04 10:35:00 UTC'}, {'name': 'To Do'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '4',  'name': 'Item 4',  'dateLastActivity': '2020-08-04 10:35:00 UTC'}, {'name': 'To Do'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '5',  'name': 'Item 5',  'dateLastActivity': '2020-08-04 10:35:00 UTC'}, {'name': 'Doing'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '6',  'name': 'Item 6',  'dateLastActivity': '2020-08-04 10:35:00 UTC'}, {'name': 'Doing'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '7',  'name': 'Item 7',  'dateLastActivity': '2020-08-04 10:35:00 UTC'}, {'name': 'Doing'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '8',  'name': 'Item 8',  'dateLastActivity': '2020-08-04 10:35:00 UTC'}, {'name': 'Doing'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '9',  'name': 'Item 9',  'dateLastActivity': '2020-08-07 10:35:00 UTC'}, {'name': 'Done'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '10', 'name': 'Item 10', 'dateLastActivity': '2020-08-07 10:35:00 UTC'}, {'name': 'Done'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '11', 'name': 'Item 11', 'dateLastActivity': '2020-08-07 10:35:00 UTC'}, {'name': 'Done'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '12', 'name': 'Item 12', 'dateLastActivity': '2020-08-07 10:35:00 UTC'}, {'name': 'Done'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '13', 'name': 'Item 13', 'dateLastActivity': '2020-08-03 10:35:00 UTC'}, {'name': 'Done'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '14', 'name': 'Item 14', 'dateLastActivity': '2020-08-03 10:35:00 UTC'}, {'name': 'Done'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '15', 'name': 'Item 15', 'dateLastActivity': '2020-08-03 11:35:00 UTC'}, {'name': 'Done'}))
    test_items.append(trello.Item.fromTrelloCard({'id': '16', 'name': 'Item 16', 'dateLastActivity': '2020-08-03 11:35:00 UTC'}, {'name': 'Done'}))
    return test_items

class TestFilters:
    @staticmethod
    def test_outstanding_item_filter(test_items):
        # Arrange
        # Act
        view = ViewModel(test_items)
        filtered_items = view.to_do_items
        # Assert
        assert any(x.status == 'To Do' for x in filtered_items)
        assert not any(x.status == 'Doing' for x in filtered_items)
        assert not any(x.status == 'Done' for x in filtered_items)
    
    @staticmethod
    def test_pending_item_filter(test_items):
        # Arrange
        # Act
        view = ViewModel(test_items)
        filtered_items = view.doing_items
        # Assert
        assert not any(x.status == 'To Do' for x in filtered_items)
        assert any(x.status == 'Doing' for x in filtered_items)
        assert not any(x.status == 'Done' for x in filtered_items)

    @staticmethod
    def test_show_all_done_items(test_items):
        # Arrange
        # Act
        view = ViewModel(test_items)
        filtered_items = view.all_done_items
        # Assert
        assert any(x.id == '9' for x in filtered_items)
        assert any(x.id == '10' for x in filtered_items)
        assert any(x.id == '11' for x in filtered_items)
        assert any(x.id == '12' for x in filtered_items)
        assert any(x.id == '13' for x in filtered_items)
        assert any(x.id == '14' for x in filtered_items)
        assert any(x.id == '15' for x in filtered_items)
        assert any(x.id == '16' for x in filtered_items)

    @staticmethod
    def test_recent_done_items(test_items, monkeypatch):
        target = datetime.date(2020, 8, 7)
        with mock.patch.object(datetime, 'date', mock.Mock(wraps=datetime.date)) as patched:
            patched.today.return_value = target
            # Act
            view = ViewModel(test_items)
            filtered_items = view.recent_done_items
            # Assert
            assert any(x.id == '9' for x in filtered_items)
            assert any(x.id == '10' for x in filtered_items)
            assert any(x.id == '11' for x in filtered_items)
            assert any(x.id == '12' for x in filtered_items)
            assert not any(x.id == '13' for x in filtered_items)
            assert not any(x.id == '14' for x in filtered_items)
            assert not any(x.id == '15' for x in filtered_items)
            assert not any(x.id == '16' for x in filtered_items)

    @staticmethod
    def test_older_done_items(test_items):
        target = datetime.date(2020, 8, 7)
        with mock.patch.object(datetime, 'date', mock.Mock(wraps=datetime.date)) as patched:
            patched.today.return_value = target
            # Act
            view =  ViewModel(test_items)
            filtered_items = view.older_done_items
            # Assert
            assert not any(x.id == '9' for x in filtered_items)
            assert not any(x.id == '10' for x in filtered_items)
            assert not any(x.id == '11' for x in filtered_items)
            assert not any(x.id == '12' for x in filtered_items)
            assert any(x.id == '13' for x in filtered_items)
            assert any(x.id == '14' for x in filtered_items)
            assert any(x.id == '15' for x in filtered_items)
            assert any(x.id == '16' for x in filtered_items)
import datetime

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return [item for item in self._items if item.status == 'To Do']
    
    @property
    def doing_items(self):
        return [item for item in self._items if item.status == 'Doing']

    @property
    def all_done_items(self):
        return [item for item in self._items if item.status == 'Done']

    @property
    def recent_done_items(self):
        return [item for item in self._items if item.status == 'Done' and item.editDatetime.date() == datetime.date.today()]

    @property
    def older_done_items(self):
        return [item for item in self._items if item.status == 'Done' and item.editDatetime.date() < datetime.date.today()]
    
    @property
    def done_items_count(self):
        all_done_items = [item for item in self._items if item.status == 'Done']
        return len(all_done_items)
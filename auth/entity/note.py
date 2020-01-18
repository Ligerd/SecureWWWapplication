import json

class Note:
    def __init__(self, id, user_id, shortcut, note,access):
        self.id = id
        self.shortcut = shortcut
        self.note = note
        self.user_id = user_id
        self.access=access


    @classmethod
    def from_json(cls, data):
        return cls(**data)
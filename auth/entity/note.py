import json

class Note:
    def __init__(self, id, user_id, shortcut, note):
        self.id = id
        self.shortcut = shortcut
        self.note = note
        self.user_id = user_id


    @classmethod
    def from_json(cls, data):
        return cls(**data)
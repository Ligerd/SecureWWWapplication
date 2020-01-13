import json

class User:
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    @classmethod
    def from_json(cls, data):
        return cls(**data)
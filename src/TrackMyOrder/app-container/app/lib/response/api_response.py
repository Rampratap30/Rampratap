import json


class APIResponse:
    def __init__(self, data=None, links=None, meta=None, errors=None):
        self.data = data
        self.links = links
        self.meta = meta
        self.errors = errors

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

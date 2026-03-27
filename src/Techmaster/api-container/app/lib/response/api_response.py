import json

from flask_restful import request

import initialize


class APIResponse:
    def __init__(self, data=None, links=None, meta=None, errors=None):
        self.data = data
        self.links = links
        self.meta = meta
        self.errors = errors
        initialize.log.write_log(str(request.full_path))
        if errors != None:
            initialize.log.write_log("Response Error : " + str(errors))

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

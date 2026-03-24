import json, os
from app.lib.aws.logger import logger
import initialize


class GenerateAPIUrl:
    def __init__(self) -> None:
        self.get_url = []
        self.post_url = []
        self.put_url = []
        main_dir = "app/service/apiURL/"
        dir_list = os.listdir(os.path.join(os.path.dirname(main_dir)))
        for dir in dir_list:
            json_files = [
                filename
                for filename in os.listdir(main_dir + dir)
                if filename.endswith(".json")
            ]
            if json_files:
                for file_name in json_files:
                    l_get_url = self.api_add_get_url(main_dir, dir, file_name)
                    if l_get_url is not None:
                        self.get_url += l_get_url

    def api_add_get_url(self, *args):
        file = open(args[0] + args[1] + "/" + args[2], "r")
        data = json.loads(file.read())
        if data["request"].get("GET"):
            return data["request"]["GET"]
        else:
            return

import json, os
from app.lib.aws.logger import logger


class techMasterAPIUrl:
    def __init__(self) -> None:
        self.get_url = []
        self.post_url = []
        self.put_url = []
        mainDir = "app/service/apiURL/"
        dirList = os.listdir(os.path.join(os.path.dirname(mainDir)))
        for dir in dirList:
            jsonFiles = [
                filename
                for filename in os.listdir(mainDir + dir)
                if filename.endswith(".json")
            ]
            if jsonFiles:
                for fileName in jsonFiles:
                    l_get_URL = self.apiAddGetUrl(mainDir, dir, fileName)
                    l_post_URL = self.apiAddPostUrl(mainDir, dir, fileName)
                    l_put_URL = self.apiAddPutUrl(mainDir, dir, fileName)
                    if l_get_URL is not None:
                        self.get_url += l_get_URL
                    if l_post_URL is not None:
                        self.post_url += l_post_URL
                    if l_put_URL is not None:
                        self.put_url += l_put_URL

    def apiAddGetUrl(self, *args):
        file = open(args[0] + args[1] + "/" + args[2], "r")
        data = json.loads(file.read())
        if data["request"].get("GET"):
            return data["request"]["GET"]
        else:
            return

    def apiAddPostUrl(self, *args):
        file = open(args[0] + args[1] + "/" + args[2], "r")
        data = json.loads(file.read())
        if data["request"].get("POST"):
            return data["request"]["POST"]
        else:
            return

    def apiAddPutUrl(self, *args):
        file = open(args[0] + args[1] + "/" + args[2], "r")
        data = json.loads(file.read())
        if data["request"].get("PUT"):
            return data["request"]["PUT"]
        else:
            return

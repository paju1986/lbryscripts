import os
import requests
import json

path = os.getcwd()
with os.scandir(path) as entries:
    for entry in entries:
        fileNameNoExtension = entry.name.split(".")[0]
        params = {
            "method": "publish",
            "params": {
                "name": fileNameNoExtension,
                "bid": "0.1",
                "file_path": path + "/" + entry.name,
                "validate_file": "false",
                "optimize_file": "false",
                "tags": [],
                "languages": [],
                "locations": [],
                "channel_id": "9e2e0f84a68146c0d13184cbf4ec3c7f4bdd1028",
                "funding_account_ids": [],
                "preview": "false",
                "preview": "false",
                "blocking": "true"
                }
        }
        print(json.dumps(params))
        requests.post("http://localhost:5279/",json.dumps(params)).json()

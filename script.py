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
                "validate_file": False,
                "optimize_file": False,
                "tags": [],
                "languages": [],
                "locations": [],
                "channel_id": "",
                "funding_account_ids": [],
                "preview": False,
                "blocking": False
                }
        }
        #print(json.dumps(params))
        print(requests.post("http://localhost:5279/",json.dumps(params)).json())
 

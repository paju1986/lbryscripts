import os
import requests
import json

path = os.getcwd()
with os.scandir(path) as entries:
    for entry in entries:
        if entry.is_file():
            thumbUrl = ""
            fileNameNoExtension = entry.name.split(".")[0]
            if entry.name.split(".")[1] == "mp4":
                thumbName = fileNameNoExtension + "_thumbnail.png"
                os.system("ffmpeg -i "+path + "/" + entry.name+" -ss 00:00:01.000 -vframes 1 "+ path + "/" + thumbName)
                thumbnailParams = {
                    "name": thumbName
                }
                files = {'file': open(path + "/" + thumbName,'rb')}

                returnJson = requests.post("https://spee.ch/api/claim/publish", files=files,data=thumbnailParams).json()
                print(returnJson)
                thumbUrl = returnJson["data"]["serveUrl"]

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
                    "channel_id": "e288b001fb5707890b637ced51bfaf8e9ced7837",
                    "thumbnail_url": thumbUrl,
                    "funding_account_ids": [],
                    "preview": False,
                    "blocking": False
                    }
            }
            #print(json.dumps(params))
            print(requests.post("http://localhost:5279/",json.dumps(params)).json())

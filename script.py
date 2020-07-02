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
                print("Creating thumbnail for file: " + entry.name + "\n")
                thumbName = fileNameNoExtension + "_thumbnail.png"
                os.system("ffmpeg -i '"+path + "/" + entry.name+"' -vcodec mjpeg -vframes 1 -an -f rawvideo -ss `ffmpeg -i '"+path + "/" + entry.name+"' 2>&1 | grep Duration | awk '{print $2}' | tr -d , | awk -F ':' '{print ($3+$2*60+$1*3600)/2}'` '"+ path + "/" + thumbName+"'")
                #os.system("ffmpeg -i '"+path + "/" + entry.name+"' -ss 00:00:01.000 -vframes 1 '"+ path + "/" + thumbName+"'")
                thumbnailParams = {
                    "name": thumbName
                }
                files = {'file': open(path + "/" + thumbName,'rb')}
                print("Uploading thumbnail to spee.ch...\n")
                reqResult = requests.post("https://spee.ch/api/claim/publish", files=files,data=thumbnailParams)
                if reqResult.status_code == 200:
                    returnJson = reqResult.json()
                    print("Finish upload thumbnail, result json: " + json.dumps(returnJson) + "\n")
                    thumbUrl = returnJson["data"]["serveUrl"]
                else: 
                    print("Spee.ch error: " + reqResult.text + "\n")
                os.remove(path + "/" + thumbName)

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
                    "channel_id": "9e2e0f84a68146c0d13184cbf4ec3c7f4bdd1028",
                    "thumbnail_url": thumbUrl,
                    "funding_account_ids": [],
                    "preview": False,
                    "blocking": False
                    }
            }
            print("Uploading file with parameters: " + json.dumps(params) + "\n")
            reqResult = requests.post("http://localhost:5279/",json.dumps(params))
            if reqResult.status_code == 200:
                returnJson = reqResult.json()
                print("Finish uploading file, result json: " + json.dumps(returnJson) + "\n")
            else:
                print("Error uploading file: " + reqResult.text + "\n")
            

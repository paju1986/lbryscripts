import os
import requests
import json
import subprocess
import sys
import getopt

### Create automated gifs of 5 seconds duration 
def createAutomatedGif(path,fileName,fileNameNoExtension): 
    thumbName = fileNameNoExtension + "_thumbnail.gif"
    vidDuration = subprocess.run(['ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "'+path + '/' + fileName + '"'],shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    vidFps = subprocess.run(['ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate "'+path + '/' + fileName + '"'],shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    fpsEncode = (float(vidDuration) / 5) * float(vidFps.split("/")[0]) 
    os.system('ffmpeg -r '+str(fpsEncode)+' -i "'+path + '/' + fileName+'" -vf "fps=1,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 "'+ path + '/' + thumbName+'"')
    return thumbName
    
### Create automated thumbnails of the middle of the file
def createAutometedThumb(path,fileName,fileNameNoExtension):
    thumbName = fileNameNoExtension + "_thumbnail.png"
    os.system("ffmpeg -i '"+path + "/" + fileName+"' -vcodec mjpeg -vframes 1 -an -f rawvideo -ss `ffmpeg -i '"+path + "/" + fileName +"' 2>&1 | grep Duration | awk '{print $2}' | tr -d , | awk -F ':' '{print ($3+$2*60+$1*3600)/2}'` '"+ path + "/" + thumbName+"'")
    return thumbName

channelId = ""
#command line arguments processing
short_options = "gc:p:t:e:"
long_options = ["createGif","channel_id=","price=","tags=","exclude="]
argument_list = sys.argv[1:]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    print(arguments)
except getopt.error as err:
    # Output error, and return with an error code
    print (str(err))
    sys.exit(2)
    
for current_argument, current_value in arguments:
    if current_argument in ("-g", "--createGif"):
        createGif = True
    elif current_argument in ("-c", "--channel_id"):
        channelId = current_value
    elif current_argument in ("-p", "--price"):
        price = current_value
    elif current_argument in ("-t", "--tags"):
        tags = current_value.split(",")
    elif current_argument in ("-e", "--exclude"):
        extExclude = current_value.split(",")
#scan current directory
path = os.getcwd()
with os.scandir(path) as entries:
    for entry in entries:
        if entry.is_file():
            thumbUrl = ""
            splitedName = entry.name.split(".")
            if not splitedName[1] in extExclude:
                fileNameNoExtension = splitedName[0]
                if len(splitedName) > 1 and splitedName[1] == "mp4":
                    print("Creating thumbnail for file: " + entry.name + "\n")
    
                    if(createGif):
                        thumbName = createAutomatedGif(path,entry.name,fileNameNoExtension)
                    else:
                        thumbName = createAutometedThumb(path,entry.name,fileNameNoExtension)
                        
                    #preparing json to send to spee.ch
                    thumbnailParams = {
                        "name": thumbName
                    }
                    files = {'file': open(path + "/" + thumbName,'rb')}
                    print("Uploading thumbnail to spee.ch...\n")
                    reqResult = requests.post("https://spee.ch/api/claim/publish", files=files,data=thumbnailParams)
                    #process response from spee.ch api
                    if reqResult.status_code == 200:
                        returnJson = reqResult.json()
                        print("Finish upload thumbnail, result json: " + json.dumps(returnJson) + "\n")
                        thumbUrl = returnJson["data"]["serveUrl"]
                    else: 
                        print("Spee.ch error: " + reqResult.text + "\n")
                    #clean temporal files
                    os.remove(path + "/" + thumbName)
                #prepare json to send to lbrynet api
                params = {
                    "method": "publish",
                    "params": {
                        "name": fileNameNoExtension.replace(" ","").replace("(","").replace(")",""),
                        "title" : fileNameNoExtension,
                        "bid": "0.1",
                        "file_path": path + "/" + entry.name,
                        "validate_file": False,
                        "optimize_file": False,
                        "tags": [],
                        "languages": [],
                        "locations": [],
                        "thumbnail_url": thumbUrl,
                        "funding_account_ids": [],
                        "preview": False,
                        "blocking": False
                        }
                }
                if(len(channelId) != 0):
                    params["params"]["channel_id"] = channelId
                if(len(price) != 0):
                    params["params"]["fee_currency"] = "lbc"
                    params["params"]["fee_amount"] = price
                if(len(tags) != 0):
                    params["params"]["tags"] = tags
                print("Uploading file with parameters: " + json.dumps(params) + "\n")
                reqResult = requests.post("http://localhost:5279/",json.dumps(params))
                if reqResult.status_code == 200:
                    returnJson = reqResult.json()
                    print("Finish uploading file, result json: " + json.dumps(returnJson) + "\n")
                else:
                    print("Error uploading file: " + reqResult.text + "\n")

                        

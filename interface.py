import glob
import os
import sys
import time
import datetime as dta
from collections import defaultdict
from flask import Flask
from string import Template
import shutil

app = Flask(__name__)
STATIC_PATH = 'static/'
CACHE_CAP = 20

def getImageInfo(imagePath):
    baseName = os.path.basename(imagePath)[:-4]
    date_time_obj = dta.datetime.strptime(baseName, "%Y%m%d-%H%M%S")

def getImageLog():
    info = defaultdict(list)
    all_images = sorted(glob.glob("static/*/*.png"))
    labeled_images, nonlabeled_images = [], []

    for img in all_images:
        if('labeled' in img):
            labeled_images.append(img)
        else:
            nonlabeled_images.append(img)
            getImageInfo(img)
            time = os.path.basename(img)[:-4][:-2]
            info[time].append(img)
    return dict(info)
        
def toFrontEnd():
    info = getImageLog()
    curFolders = sorted(glob.glob("static/*"))
    while(len(curFolders) > CACHE_CAP):
        shutil.rmtree(curFolders.pop(0))
    output = "<meta http-equiv='refresh' content='1' > <title> Person Detection Log </title> <h1> Person Detection Log </h1><br>Last Updated: "
    output += str(dta.datetime.now())[:-7] 
    output += " Local Time <br><br>"
    for k in sorted(info, reverse=True):
        output = output + "<a href='/%s'> " %k + k + ": " + str(len(info[k])) + " Events Detected </a>"
        output += "<br><br>"
    return output

@app.route('/<datetime>')
def req_file(datetime):
    info = getImageLog()
    info = info[datetime]
    info = info[::-1]
    out = "<meta http-equiv='refresh' content='1' ><title> Minute Detail Log </title><h1>  Minute Detail Log for " +  str(datetime) + "</h1><table style='width: 30%'>" 
    for img in info:
        outName = dta.datetime.strptime(os.path.basename(img)[:-4], '%Y%m%d-%H%M%S')
        out += "<tr><td><br><br>%s</td></tr>" %(outName)
        out += "<tr>"
        labeled_img = img[:-4] + "_labeled.png"
        out += "<td><img src=%s></td>" %(img)
        out += "<td><img src=%s></td>" %(labeled_img)
        out += "</tr>"
    out += "</table>" 
    return out

@app.route('/')
def main():
    return toFrontEnd()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


## Veeam Folder Synchronization Test Task
## Author: Pedro Reis

import sys
import shutil
import os
import datetime

##Set Folder and Make Sure Path Exists
def setFolder(path):
    while(not os.path.exists(path)):
        print("ERROR: Path does not Exist:\n")
        path = input('Please Input new Folder Path:\n\t')
    return path

ogFolder = setFolder(sys.argv[1])
repFolder = setFolder(sys.argv[2])
synchroTime = sys.argv[2]
logPath = setFolder(sys.argv[4]) + "\\synchroFolder_LOG.txt"

##LOG Actions
def log(action):
    global logPath
    with open(logPath, "a") as log:
        ct = datetime.datetime.now()
        action = ct.strftime("%m/%d/%y - %H:%M:%S") + ": " + action + "\n"
        log.write(action)
        print(action)
        log.close()

##Copy the contents from Source directory to Destination
def copyContents(source, dest):
    for item in os.listdir(source):
        itemPath = os.path.join(source, item)
        if os.path.isfile(itemPath):
            log("Copying File: " + item + " to " + dest)
            shutil.copyfile(itemPath, os.path.join(dest, item)) 
        else:
            log("Copying Folder: " + item + " to " + dest)
            createFolder(itemPath, dest, False) 

##Create a Folder at Specified Destination
def createFolder(source, dest, isReplica):
    tmp = source.split('\\')
    dest = os.path.join(dest, tmp[len(tmp)-1])
    if(isReplica):
        dest = dest + "_REPLICA"
    os.makedirs(dest)
    log("Created Folder: " + dest)
    copyContents(source, dest)
    return repFolder 

repFolder = createFolder(ogFolder, repFolder, True)


##TODO
def checkFiles(ogFolder, repFolder):
    ogFiles = os.listdir(ogFolder)
    repFiles = os.listdir(repFolder)

while(True):
    checkFiles(ogFolder, repFolder)
    time.sleep(synchroTime)
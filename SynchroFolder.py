## Veeam Folder Synchronization Test Task
## Author: Pedro Reis

import sys
import shutil
import os
import datetime

def setFolder(path):
    while(not os.path.exists(path)):
        print("ERROR: Path does not Exist:\n")
        path = input('Please Input new Folder Path:\n\t')
    return path

ogFolder = setFolder(sys.argv[1])
repFolder = setFolder(sys.argv[2])
synchroTime = sys.argv[2]
logPath = setFolder(sys.argv[4]) + "\\synchroFolder_LOG.txt"

def log(action):
    global logPath
    with open(logPath, "a") as log:
        ct = datetime.datetime.now()
        action = ct.strftime("%m/%d/%y - %H:%M:%S") + ": " + action + "\n"
        log.write(action)
        print(action)
        log.close()

def copyContents(source, dest):
    for item in os.listdir(source):
        itemPath = os.path.join(source, item)
        if os.path.isfile(itemPath):
            log("Copying File: " + item + " to " + dest)
            shutil.copyfile(itemPath, os.path.join(dest, item)) 
        else:
            log("Copying Folder: " + item + " to " + dest)
            createFolder(itemPath, dest, False) 


"""
        for file in files:
            log("Copying File: " + file + " to " + dest)
            shutil.copyfile(os.path.join(source, file), os.path.join(dest, file))
            ##Logging
            
        for folder in dirs:
            log("Copying Folder: " + folder + " to " + dest)
            createFolder(os.path.join(source,folder), dest, False)
"""

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


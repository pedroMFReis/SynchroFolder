## Veeam Folder Synchronization Test Task
## Author: Pedro Reis

import sys
import shutil
import os
import datetime
import time
import filecmp

##Set Folder and Make Sure Path Exists
def setFolder(path):
    while(not os.path.exists(path)):
        print("ERROR: Path does not Exist:\n")
        path = input('Please Input new Folder Path:\n\t')
    return path

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
def copyContents(source, dest, files):
    for item in files:
        itemPath = os.path.join(source, item)
        if os.path.isfile(itemPath):
            log("Created File: " + item + " to " + dest)
            shutil.copyfile(itemPath, os.path.join(dest, item)) 
        else:
            createFolder(itemPath, dest, False) 

##Create a Folder at Specified Destination
#Replica - Flag that Represents if it's main Replica Folder
def createFolder(source, dest, isReplica):
    tmp = source.split('\\')
    dest = os.path.join(dest, tmp[len(tmp)-1])
    if(isReplica):
        dest = dest + "_REPLICA"
    try:
        os.makedirs(dest)
        log("Created Folder: " + dest)
        copyContents(source, dest, os.listdir(source))
    except FileExistsError:
        log("Folder already Exists")
        updateFolder(source, dest)
    return dest


#Removes Items from given Directory
def removeItems(items, path):

    for i in items:
        iPath = os.path.join(path, i)
        if os.path.isfile(iPath):
            os.remove(iPath)
            log("Deleted File: " + i + " from " + path)
        else:
            removeItems(os.listdir(iPath), iPath)
            os.rmdir(iPath)
            log("Deleted Folder: " + i + " from " + path)

##Compared Files in Original and Replicated Folder, updating, Adding or Removing Files
def updateFolder(ogFolder, repFolder):
    ogFiles = os.listdir(ogFolder)
    repFiles = os.listdir(repFolder)

    for ogItem in ogFiles:
        
        found = False
        ogItemPath = os.path.join(ogFolder, ogItem)
        
        for repItem in repFiles:
            if ogItem == repItem:

                ##Compares Found Same Name Items in Folder
                repItemPath = os.path.join(repFolder, repItem)
                if os.path.isfile(ogItemPath): 
                    if not filecmp.cmp(ogItemPath, repItemPath):
                        shutil.copyfile(ogItemPath, repItemPath)
                        log("Copied File: " + ogItem + " to " + repFolder)
                else:
                    updateFolder(os.path.join(ogFolder, ogItem), os.path.join(repFolder, repItem))
                
                repFiles.remove(repItem)
                found = True
        
        # Creates New Item that has not been found
        if(not found):
            if os.path.isfile(ogItemPath):       
                log("Created File: " + ogItem + " in " + repFolder)
                shutil.copy(ogItemPath, repFolder)
            else:
                createFolder(ogItemPath, repFolder, False)
    
    #Removes Files that are not found in Original Folder from Replica Folder
    removeItems(repFiles, repFolder)



## Getting all arguments Provided and assingning them to variables
ogFolder = setFolder(sys.argv[1])
repFolder = setFolder(sys.argv[2])
synchroTime = sys.argv[3]
logPath = setFolder(sys.argv[4]) + "\\synchroFolder_LOG.txt"

log("Begin App\n\t Original Folder: " + ogFolder + "\n\tReplica Folder: " + repFolder + "\n\tSynchronization Time: " + synchroTime + "\n")

repFolder = createFolder(ogFolder, repFolder, True)

##Periodically Checks and Updates Replica Folder
while(True):
    updateFolder(ogFolder, repFolder)
    time.sleep(int(synchroTime))
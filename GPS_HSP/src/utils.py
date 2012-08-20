'''
Created on Oct 13, 2011

@author: hansskov-petersen
'''
import os

def getFileNameFromPath(path):
    return path.split("/")[-1]

def listFilesByExtention(path, extention, caseSensitive=False):
    if not caseSensitive:
        extention = extention.upper()
    files = os.listdir(path)
    fileList = []
    for file in files:
        fileSplit = file.split(".")
        if not caseSensitive:
            fileExtention = fileSplit[1].upper()
        if len(fileSplit) == 2:
            if fileExtention == extention:
                fileList.append(file)
    return fileList  
          
# setting a trace point in the code, for command line inspection
# import pdb;pdb.set_trace()
#coding=UTF-8
import sys
import os, glob

sys.path.append("../modules");

from ID3v1 import ID3v1

#####################Testing reading tags##########################
dirToScan = "/media/LVM/Music"

genres = {}
counter = 0

def ScanDirectory (dirPath):
    global counter
    if os.path.isdir(dirPath):
        fileList = glob.glob(dirPath+"/*")
        for everyFile in fileList:
            ScanDirectory(everyFile)
    if os.path.isfile(dirPath):
        if dirPath[-3:] == "mp3":
            f = open(dirPath, "rb")
            tag = ID3v1()
            try:
                tag.GetTag(f)
            except IOError:
                print ("No tag: ", dirPath)
            else:
                genres[tag.genre] = genres.get(tag.genre, 0) + 1
            f.close()
            counter = counter + 1
            print (counter, "\r", end="")

ScanDirectory(dirToScan)

print("\n", genres)


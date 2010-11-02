#coding=UTF-8
import sys
import os, glob

sys.path.append("../modules");

from ID3v2 import ID3Header, ID3Frame

#####################Testing reading tags##########################
dirToScan = "/media/LVM/Music"

mp3List = []
fileExtensions = {}

def ScanDirectory (dirPath):
    if os.path.isdir(dirPath):
        fileList = glob.glob(dirPath+"/*")
        for everyFile in fileList:
            ScanDirectory(everyFile)
    if os.path.isfile(dirPath):
        if dirPath[-4] == ".":
            if dirPath[-3:] in fileExtensions:
                fileExtensions[dirPath[-3:]] += 1
            else:
                fileExtensions[dirPath[-3:]] = 1
        elif dirPath[-5] == ".":
            if dirPath[-4:] in fileExtensions:
                fileExtensions[dirPath[-4:]] += 1
            else:
                fileExtensions[dirPath[-4:]] = 1
        if dirPath[-3:] == "mp3":
            mp3List.append(dirPath)
            
            f = open(dirPath, "rb")
            header = ID3Header()
            try:
                header.ReadHeader(f)
                position = 10
                while position < header.dataLength:
                    frame = ID3Frame(header)
                    frame.ReadFrame(f, position)
                    if bytes.decode(frame.header.id) == "TCON":
                        print (frame.data)
                    position =position + frame.header.headerLength + frame.header.dataLength
            except NotImplementedError:
                pass
            f.close()

            print (len(mp3List), "\r", end="")
            #print (mp3List[len(mp3List)-1], "\r", end="")


ScanDirectory(dirToScan)

print(len(mp3List))
print(fileExtensions)

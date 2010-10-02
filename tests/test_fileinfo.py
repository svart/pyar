#coding=UTF-8
import sys
import os, glob

sys.path.append("../modules");

from FileInfo import FileInformation

#####################################
filePath = "/media/LVM/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3"
filePath2 = "/media/LVM/Music/Dawn of Tears/2007 - Descent/03 - Lost Verses.mp3"
filePath3 = "/media/LVM/Music/Godsmack/2010 - The Oracle/02 - Saint And Sinners.mp3"

fileInfo = FileInformation(filePath)

print (fileInfo.FileSize("M"))
print (fileInfo.FileAccessTime())
print (fileInfo.fullPath)
print (fileInfo.dirName)
print (fileInfo.fileName)

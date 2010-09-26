# -*- coding: UTF8 -*-
import sys
sys.path.append("modules");

from ID3Header import ID3Header
from FileInfo import FileInformation
#from ID3FrameHeader import ID3FrameHeader
from ID3Frame import ID3Frame

#####################Testing reading tags##########################
filePath = "/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3"
filePath2 = "/media/FreeAgent/Music/Dawn of Tears/2007 - Descent/03 - Lost Verses.mp3"
filePath3 = "/media/FreeAgent/Music/Godsmack/2010 - The Oracle/02 - Saint And Sinners.mp3"
f = open(filePath3, "rb");

header = ID3Header()
header.ReadHeader(f)

print "Version/Subversion: ", header.version, "/", header.subversion
print "Header Flags: ", header.flags
print "Length Of Tags: ", header.dataLength
print ""

#####################Testing getting file info##########################
#fileInfo = FileInformation()       
        
#print fileInfo.GetFileSizeByPath("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3", "M");
#print fileInfo.GetFileAccessTime("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3")
#print fileInfo.GetFileModificationTime("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3")

#frameHeader = ID3FrameHeader(10)
#frameHeader.ReadHeader(f)


frames = []

position = 10
while position < header.dataLength:
    frame = ID3Frame()
    frame.ReadFrame(f, position)
    frames.append(frame)
    position =position + frame.header.headerLength + frame.header.dataLength
    print position, " ",

for frame in frames:
    print "Frame ID: ", frame.header.id
    print "Frame Data Length: ", frame.header.dataLength
    print "Frame Flags: ", frame.header.flags
    print "Frame Data: ", frame.data

f.close()

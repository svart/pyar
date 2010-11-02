#coding=UTF-8
import sys
sys.path.append("../modules")

from ID3v2 import ID3Header, ID3Frame

#####################Testing reading tags##########################
filePath = "/media/LVM/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3"
filePath2 = "/media/LVM/Music/Dawn of Tears/2007 - Descent/03 - Lost Verses.mp3"
filePath3 = "/media/LVM/Music/Godsmack/2010 - The Oracle/02 - Saint And Sinners.mp3"
encryptFilePath = "/media/LVM/Music/Children of Bodom/1997 - Children Of Bodom/01 - Children Of Bodom.mp3"
filePath4 = "./01.mp3"
f = open(filePath4, "rb");

header = ID3Header()
header.ReadHeader(f)

print("Version/Subversion: ", header.version, "/", header.subversion)
print("Header Flags: ", header.flags)
print("Length Of Tags: ", header.dataLength)
print("")

#####################Testing##########################

frames = []

position = 10
while position < header.dataLength:
    frame = ID3Frame(header)
    frame.ReadFrame(f, position)
    frames.append(frame)
    position =position + frame.header.headerLength + frame.header.dataLength

for frame in frames:
    if frame.header.dataLength != 0:
        print("Frame ID: ", bytes.decode(frame.header.id))
        print("Frame Data Length: ", frame.header.dataLength)
        print("Frame Flags: ", frame.header.flags)
        print("Frame Data: ", frame.data, " => ")# , bytes.decode(frame.data), "\n")

f.close()

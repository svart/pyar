#coding=UTF-8
import sys
sys.path.append("../modules")

from MPEGInfo import MPEGInfo
from ID3v2 import ID3Header, ID3Frame

#####################Testing reading tags##########################
filePath = "/media/LVM/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3"
filePath2 = "/media/LVM/Music/Dawn of Tears/2007 - Descent/03 - Lost Verses.mp3"
filePath3 = "/media/LVM/Music/Godsmack/2010 - The Oracle/02 - Saint And Sinners.mp3"
encryptFilePath = "/media/LVM/Music/Children of Bodom/1997 - Children Of Bodom/01 - Children Of Bodom.mp3"
longName = "/media/LVM/Music/The Project Hate MCMXCIX/2005 - Armageddon March Eternal (Symphonies Of Slit Wrists)/06 - Godslaughtering Murder Machine.mp3"

f = open(filePath, "rb");

header = ID3Header()
header.ReadHeader(f)

info = MPEGInfo()


info.ReadInfo(f, header.dataLength)

print ("Byte Header: ", info.byteHeader)
print ("MPEG version: ", info.MPEGVersion)
print ("Layer index: ", info.layer)
print ("Has protection: ", info.protected)
print ("Samle Rate: ", info.sampleRate)
print ("BitRate: ", info.bitRate)
print ("Channel Mode: ", info.channelMode)

f.close()

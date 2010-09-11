# -*- coding: UTF8 -*-
import sys
sys.path.append("modules");

from ID3Header import ID3Header
from FileInfo import FileInformation

#####################Testing reading tags##########################
filePath = "/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3";
f = open(filePath, "rb");

header = ID3Header()
header.ReadHeader(f)

print header.dataLength, header.flags, header.version

#####################Testing getting file info##########################
fileInfo = FileInformation()       
        
print fileInfo.GetFileSizeByPath("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3", "M");
print fileInfo.GetFileAccessTime("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3")
print fileInfo.GetFileModificationTime("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3")



# -*- coding: UTF8 -*-

from ID3Header import ID3Header

#####################Testing##########################

filePath = "/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3";
f = open(filePath, "rb");

header = ID3Header()
header.ReadHeader(f)

print header.dataLength, header.flags, header.version


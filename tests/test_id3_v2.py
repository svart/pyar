#coding=UTF-8
import sys
sys.path.append("../modules")

import optparse, ID3v2


parser = optparse.OptionParser(usage="usage: %prog path")
(options, args) = parser.parse_args()

if len(args)==1:
    filePath = args[0]
    print("Getting tag:",filePath, "\n")

    f = open(filePath, "rb");
    tag = ID3v2.ID3v2Tag()
    
    tag.ReadTag(f)
    
    print("Version/Subversion: ", tag.header.version, "/", tag.header.subversion)
    print("Header Flags: ", tag.header.flags)
    print("Length Of Tags: ", tag.header.dataLength)
    print("")


    print("Исполнитель:", tag.tagList["TPE1"].value)
    print("Альбом:", tag.tagList["TALB"].value)
    print("Название:", tag.tagList["TIT2"].value)
    print("Жанр:", tag.tagList["TCON"].value)
    print("Дорожка:", tag.tagList["TRCK"].value)
    print("Год:", tag.tagList["TDRC"].value)
    for frameName in tag.tagList.keys():
        if frameName not in tag.supportedTags and tag.tagList[frameName].header.dataLength != 0:
            print (tag.tagList[frameName].header.id.decode(), ":", end="")
            try:
                print (tag.tagList[frameName].data.decode("UTF-8"))
            except (UnicodeDecodeError, AttributeError):
                print ("DECODING ERROR")

    f.close()

else:
    print("ERROR: There must be only one argument. Use option -h/--help to see help page.")
    


#print("Frame ID: ", bytes.decode(frame.header.id))
#print("Frame Data Length: ", frame.header.dataLength)
#print("Frame Flags: ", frame.header.flags)
#print("Frame Data: ", bytes.decode(frame.data), "\n")

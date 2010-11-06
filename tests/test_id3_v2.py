#coding=UTF-8
import sys
sys.path.append("../modules")

from ID3v2 import ID3v2Tag
import optparse


parser = optparse.OptionParser(usage="usage: %prog path")
(options, args) = parser.parse_args()

if len(args)==1:
    filePath = args[0]
    print("Getting tag:",filePath, "\n")

    f = open(filePath, "rb");
    tag = ID3v2Tag()
    
    tag.ReadTag(f)
    
    print("Version/Subversion: ", tag.header.version, "/", tag.header.subversion)
    print("Header Flags: ", tag.header.flags)
    print("Length Of Tags: ", tag.header.dataLength)
    print("")


    for frame in tag.tagList:
        if frame.header.dataLength != 0:# and bytes.decode(frame.header.id) != 'APIC':
            try:
                print (bytes.decode(frame.header.id), ":", bytes.decode(frame.data))
            except UnicodeDecodeError:
                print (bytes.decode(frame.header.id), ": DECODING ERROR")

    f.close()

else:
    print("ERROR: There must be only one argument. Use option -h/--help to see help page.")
    


#print("Frame ID: ", bytes.decode(frame.header.id))
#print("Frame Data Length: ", frame.header.dataLength)
#print("Frame Flags: ", frame.header.flags)
#print("Frame Data: ", bytes.decode(frame.data), "\n")

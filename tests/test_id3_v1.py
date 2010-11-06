#coding=UTF-8
import sys
sys.path.append("../modules")

from ID3v1 import ID3v1, ID3v1NoTagError
import optparse

parser = optparse.OptionParser(usage="usage: %prog path")
(options, args) = parser.parse_args()

if len(args)==1:
    filePath = args[0]
    print("Getting tag:",filePath)

    f = open(filePath, "rb");
    tag = ID3v1()

    try:
        tag.GetTag(f)
        print("Название:", tag.title.decode())
        print("Исполнитель:", bytes.decode(tag.artist))
        print("Альбом:", bytes.decode(tag.album))
        print("Год:", bytes.decode(tag.year))
        print("Комментарий:", bytes.decode(tag.comment))
        print("Жанр:", tag.genre)
        print("Номер трека:", tag.track)
    except ID3v1NoTagError:
        print ("Error:", filePath, "has no ID3v1 tag")

    f.close()
    
else:
    print("ERROR: There must be only one argument. Use option -h/--help to see help page.")
    

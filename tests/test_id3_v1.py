#coding=UTF-8
import sys
sys.path.append("../modules")

from ID3v1 import ID3v1

#####################Testing reading tags##########################
filePath = "/media/LVM/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3"
filePath2 = "/media/LVM/Music/Dawn of Tears/2007 - Descent/03 - Lost Verses.mp3"
filePath3 = "/media/LVM/Music/Godsmack/2010 - The Oracle/02 - Saint And Sinners.mp3"
encryptFilePath = "/media/LVM/Music/Children of Bodom/1997 - Children Of Bodom/01 - Children Of Bodom.mp3"
longName = "/media/LVM/Music/The Project Hate MCMXCIX/2005 - Armageddon March Eternal (Symphonies Of Slit Wrists)/06 - Godslaughtering Murder Machine.mp3"
f = open(longName, "rb");

tag = ID3v1()
tag.GetTag(f)

print("Название: ", bytes.decode(tag.title))
print("Исполнитель: ", bytes.decode(tag.artist))
print("Альбом: ", bytes.decode(tag.album))
print("Год: ", bytes.decode(tag.year))
print("Комментарий: ", bytes.decode(tag.comment))
print("Жанр: ", tag.genre)
print("Номер трека: ", tag.track)

f.close()

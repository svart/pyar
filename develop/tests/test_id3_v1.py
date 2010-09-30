#coding=UTF-8
import sys
sys.path.append("../modules")

from ID3v1 import ID3v1

#####################Testing reading tags##########################
filePath = "/media/LVM/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3"
filePath2 = "/media/LVM/Music/Dawn of Tears/2007 - Descent/03 - Lost Verses.mp3"
filePath3 = "/media/LVM/Music/Godsmack/2010 - The Oracle/02 - Saint And Sinners.mp3"
f = open(filePath, "rb");

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

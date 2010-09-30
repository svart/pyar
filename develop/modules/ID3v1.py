#coding=UTF-8

class ID3v1(object):
    """ Модуль для анализа ID3v1 тегов.
    """
    
    def __init__(self):
        self.title = ""
        self.artist = ""
        self.album = ""
        self.year = ""
        self.comment = ""
        self.genre = ""
        self.track = ""
    
    def GetTag(self, music_file):
        music_file.seek(-128, 2)        #128 байт с конца файла
        ID = music_file.read(3)
        print (ID)
        
        if ID != b"TAG":
            raise ValueError('This file does not have ID3v1 tag.')
        
        self.title = music_file.read(30)
        self.artist = music_file.read(30)
        self.album = music_file.read(30)
        self.year = music_file.read(4)
        self.comment = music_file.read(30)
        genreId = music_file.read(1)
        
        if self.comment[28] == 0:
            self.track = self.comment[29]
            self.comment = self.comment[:28]
            
        self.genre = self.GetGenreByID(genreId)

    def GetGenreByID(self, ID):
        if ID == b"\xFF":
            return "No genre"


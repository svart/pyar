#coding=UTF-8

class ID3Header:
    def __init__(self):
        self.FIRST_BIT = 0x01
        self.FLAG_OFFSET = {"UNSYNCH":7, "EXTHEADER":6, "EXPERIMENT":5, "FOOTERPRES":4}
        self.dataLength = 0
        self.marker = ""
        self.version = 0
        self.subversion = 0
        self.flags = {}
    
    def GetMarker(self, music_file):
        """Возвращает ID3 маркер файла"""
        currentPosition = music_file.tell()     #Запомнили текущую позицию в файле
        music_file.seek(0)                      #Сместились в начало файла
        marker = music_file.read(3)             #Прочитали 3 байта, которые должны содержать "ID3"
        music_file.seek(currentPosition)        #Вернули предыдущую позицию в файле
        return marker
    
    def GetDataLength(self, music_file):
        """Возвращает длину поля данных ID3 тега"""
        currentPosition = music_file.tell()
        music_file.seek(6)
        byteLength = music_file.read(4)
        id3Length = 0
        for x in byteLength:
            id3Length = id3Length*128 + x%128
        music_file.seek(currentPosition)    
        return id3Length
        
    def GetVersions(self, music_file):
        """Возвращает кортеж: (версия, подверсия)"""
        currentPosition = music_file.tell()
        music_file.seek(3)
        version = music_file.read(1)
        subversion = music_file.read(1)
        music_file.seek(currentPosition)
        return ord(version), ord(subversion)
     
    def GetFlags(self, music_file):
        """Возвращает флаги в заголовке тега"""
        currentPosition = music_file.tell()
        music_file.seek(5)
        
        bitFlags = music_file.read(1)
        flags = {}
        for key in self.FLAG_OFFSET:
            flags[key] = ord(bitFlags)>>self.FLAG_OFFSET[key] & self.FIRST_BIT
            
        music_file.seek(currentPosition)
        return flags

    def ReadHeader(self, music_file):
        """Читает заголовок ID3 тега"""
        self.marker = self.GetMarker(music_file)
        if self.marker != b'ID3':
            raise ValueError('This file does not have ID3 Header.')
            
        self.dataLength = self.GetDataLength(music_file)
        
        self.version, self.subversion = self.GetVersions(music_file)
        
        self.flags = self.GetFlags(music_file)

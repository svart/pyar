#coding=UTF-8

class ID3Header:
    def __init__(self):
        self.dataLength = 0
        self.marker = ""
        self.version = 0
        self.subversion = 0
        self.flags = {"a":0,        #Unsynchronisation – используется только с MPEG-2 и MPEG-2.5 форматами.
                      "b":0,        #Extended header – указывает на наличие расширенного заголовка
                      "c":0,        #Experimental indicator – эксперементальный индикатор
                      "d":0}        #Footer present - только для ID3v2.4.0
    
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
        flags = music_file.read(1)
        aFlag = ord(flags)/128
        bFlag = ord(flags)%128/64
        cFlag = ord(flags)%64/32
        dFlag = ord(flags)%32/16
        music_file.seek(currentPosition)
        return [aFlag, bFlag, cFlag, dFlag]

    def ReadHeader(self, music_file):
        """Читает заголовок ID3 тега"""
        self.marker = self.GetMarker(music_file)
        if self.marker != b'ID3':
            raise ValueError('This file does not have ID3 Header.')
            
        self.dataLength = self.GetDataLength(music_file)
        
        self.version, self.subversion = self.GetVersions(music_file)
        
        flags = self.GetFlags(music_file)
        self.flags = dict(zip(self.flags.keys(),flags))

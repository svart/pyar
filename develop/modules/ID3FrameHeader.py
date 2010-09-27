# -*- coding: UTF8 -*-

class ID3FrameHeader:
    """Основной объект ID3 тега
    
    Это базовый класс для различных видов тегов.
    """

    FLAG23_ALTERTAG     = 0x8000
    FLAG23_ALTERFILE    = 0x4000
    FLAG23_READONLY     = 0x2000
    FLAG23_COMPRESS     = 0x0080
    FLAG23_ENCRYPT      = 0x0040
    FLAG23_GROUP        = 0x0020

    FLAG24_ALTERTAG     = 0x4000
    FLAG24_ALTERFILE    = 0x2000
    FLAG24_READONLY     = 0x1000
    FLAG24_GROUPID      = 0x0040
    FLAG24_COMPRESS     = 0x0008
    FLAG24_ENCRYPT      = 0x0004
    FLAG24_UNSYNCH      = 0x0002
    FLAG24_DATALEN      = 0x0001
    
    def __init__(self):
        self.startPosition = 0
        self.dataLength = 0
        self.headerLength = 10      #По умолчанию заголовок фрейма равен 10 байтам.
        self.id = ""
        self.flags = 0

    def GetId(self, music_file):
        currentPosition = music_file.tell()
        music_file.seek(self.startPosition)
        frameId = music_file.read(4)
        music_file.seek(currentPosition)    
        return frameId
        
    def GetSize(self, music_file):
        currentPosition = music_file.tell()
        music_file.seek(self.startPosition + 4)
        byteLength = music_file.read(4)
        frameLength = 0
        for x in byteLength:
            frameLength = frameLength*256 + x%256
        music_file.seek(currentPosition)    
        return frameLength
        
    def GetFlags(self, music_file):
        currentPosition = music_file.tell()
        music_file.seek(self.startPosition+8)
        flags = music_file.read(2)              #Читаем 2 байта флагов
        music_file.seek(currentPosition)
        return flags
        
    def ReadHeader(self, music_file, startPosition):  
        self.startPosition = startPosition      
        self.id = self.GetId(music_file)
        self.dataLength = self.GetSize(music_file)
        self.flags = self.GetFlags(music_file)


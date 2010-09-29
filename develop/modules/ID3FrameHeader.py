# -*- coding: UTF8 -*-

class ID3FrameHeader:
    """Заголовок фрейма в ID3 теге
    """

    FIRST_BIT = 0x0001
    FLAG23_OFFSET = {"ALTERTAG":15, "ALTERFILE":14, "READONLY":13, "COMPRESS":7, "ENCRYPT":6, "GROUP":5}
    FLAG24_OFFSET = {"ALTERTAG":14, "ALTERFILE":13, "READONLY":12, "GROUPID":6, "COMPRESS":3, "ENCRYPT":2, "UNSYNCH":1, "DATALEN":0}
    

    def __init__(self):
        self.startPosition = 0
        self.dataLength = 0
        self.headerLength = 10      #По умолчанию заголовок фрейма равен 10 байтам.
        self.id = ""
        self.flags = {}

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
        
    def GetFlags(self, music_file, version):
        currentPosition = music_file.tell()
        music_file.seek(self.startPosition+8)
        
        byte1 = music_file.read(1)              #Последовательное чтение двух байт флагов
        byte2 = music_file.read(1)
        bitFlags = ord(byte1)*256 + ord(byte2)  #Преобразование byte в int
        flags = {}
        
        if version == 3:
            for key in ID3FrameHeader.FLAG23_OFFSET:
                flags[key] = bitFlags>>ID3FrameHeader.FLAG23_OFFSET[key] & ID3FrameHeader.FIRST_BIT

        if version == 4:
            for key in ID3FrameHeader.FLAG24_OFFSET:
                flags[key] = bitFlags>>ID3FrameHeader.FLAG24_OFFSET[key] & ID3FrameHeader.FIRST_BIT
        
        music_file.seek(currentPosition)
        return flags
        
    def ReadHeader(self, music_file, startPosition, version):  
        self.startPosition = startPosition      
        self.id = self.GetId(music_file)
        self.dataLength = self.GetSize(music_file)
        self.flags = self.GetFlags(music_file, version)


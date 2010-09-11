# -*- coding: UTF8 -*-

class ID3FrameHeader:
    def __init__(self):
        self.startPosition = 0
        self.dataLength = 0
        self.headerLength = 10      #По умолчанию заголовок фрейма равен 10 байтам. TODO:Обработать другие случаи в зависимости от флагов
        self.id = ""
        self.flags = {"a":0,        #
                      "b":0,        #
                      "c":0,        #
                      "i":0,        #
                      "j":0,        #
                      "k":0}        #

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
            frameLength = frameLength*256 + ord(x)%256
        music_file.seek(currentPosition)    
        return frameLength
        
    def GetFlags(self, music_file):
        currentPosition = music_file.tell()
        music_file.seek(self.startPosition+8)
        flags = music_file.read(1)
        aFlag = ord(flags)/128
        bFlag = ord(flags)%128/64
        cFlag = ord(flags)%64/32
        flags = music_file.read(1)
        iFlag = ord(flags)/128
        jFlag = ord(flags)%128/64
        kFlag = ord(flags)%64/32
        music_file.seek(currentPosition)
        return [aFlag, bFlag, cFlag, iFlag, jFlag, kFlag]
        
    def ReadHeader(self, music_file, startPosition):  
        self.startPosition = startPosition      
        self.id = self.GetId(music_file)
        self.dataLength = self.GetSize(music_file)
        flags = self.GetFlags(music_file)
        self.flags = dict(zip(self.flags.keys(),flags))


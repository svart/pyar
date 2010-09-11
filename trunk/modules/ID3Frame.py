# -*- coding: UTF8 -*-

from ID3FrameHeader import ID3FrameHeader

class ID3Frame:
    def __init__(self):
        self.startPosition = 0
        self.header = ID3FrameHeader()
        self.data = 0
    
    def ReadData(self, music_file):
        currentPosition = music_file.tell()
        music_file.seek(self.startPosition+self.header.headerLength)
        data = music_file.read(self.header.dataLength)
        music_file.seek(currentPosition)
        return data
    
    def ReadFrame(self, music_file, startPosition):
        self.startPosition = startPosition
        self.header.ReadHeader(music_file, startPosition)
        self.data = self.ReadData(music_file)

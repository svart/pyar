# -*- coding: UTF8 -*-

import struct
from zlib import error as zlibError
from ID3FrameHeader import ID3FrameHeader

class ID3Frame:
    """Основной объект ID3 тега
    
    Это базовый класс для различных видов тегов.
    """

    def __init__(self, id3Header):
        self.startPosition = 0
        self.id3Header = id3Header
        self.header = ID3FrameHeader(id3Header.version)
        self.data = 0
    
    def decode(self, value):
        output = []
        safe = True
        append = output.append
        for val in value:
            if safe:
                append(chr(val))
                safe = val != '\xFF'
            else:
                if val >= '\xE0': raise ValueError('invalid sync-safe string')
                elif val != '\x00': append(chr(val))
                safe = True
        if not safe: raise ValueError('string ended unsafe')
        return "".join(output)
    
    def ReadData(self, music_file):
        currentPosition = music_file.tell()
        music_file.seek(self.startPosition+self.header.headerLength)
        data = music_file.read(self.header.dataLength)
        
        if self.id3Header.version == 4:
            if self.header.flags["COMPRESS"] and self.header.flags["DATALEN"]: 
                dataBytes = data[:4]
                data = data[4:]

            if self.header.flags["UNSYNCH"] or self.id3Header.flags["UNSYNCH"]:     #Стыбжено из mutagen
                output = []
                safe = True
                append = output.append
                for val in data:
                    if safe:
                        append(chr(val))
                        safe = val != '\xFF'
                    else:
                        if val >= '\xE0': raise ValueError("Invalid sync-safe string")
                        elif val != '\x00': append(chr(val))
                        safe = True
                if not safe: raise ValueError("String ended unsafe")
                data = "".join(output)
                
            if self.header.flags["ENCRYPT"]:
                raise NotImplementedError("Encryption is not supported")
                
            if self.header.flags["COMPRESS"]: 
                try: data = data.decode('zlib')
                except zlibError:
                    data = dataBytes + data
                    data = data.decode('zlib')
                
        elif self.id3Header.version == 3:
            if self.header.flags["COMPRESS"]:
                usize, = struct.unpack('>L', data[:4])                      #Разобраться, что это за хрень!!!
                data = data[4:]
            
            if self.header.flags["ENCRYPT"]:
                raise NotImplementedError("Encryption is not supported")
                
            if self.header.flags["COMPRESS"]:
                data = data.decode('zlib')

        music_file.seek(currentPosition)

        return data
    
    def ReadFrame(self, music_file, startPosition):
        self.startPosition = startPosition
        self.header.ReadHeader(music_file, startPosition)
        self.data = self.ReadData(music_file)

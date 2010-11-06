#coding=UTF-8

class ID3Header:
    """Заголовок ID3 тега 2й версии. 
       Располагается вначале файла, перед аудиоданными.
    """
    
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
        

class ID3FrameHeader:
    """Заголовок фрейма в ID3 теге.
    
       ID3 состоит из заголовка и следующими за ним фреймами.
    """

    def __init__(self, version):
        self.FIRST_BIT = 0x0001
        self.FLAG23_OFFSET = {"ALTERTAG":15, "ALTERFILE":14, "READONLY":13, "COMPRESS":7, "ENCRYPT":6, "GROUP":5}
        self.FLAG24_OFFSET = {"ALTERTAG":14, "ALTERFILE":13, "READONLY":12, "GROUPID":6, "COMPRESS":3, "ENCRYPT":2, "UNSYNCH":1, "DATALEN":0}

        self.startPosition = 0
        self.dataLength = 0
        self.headerLength = 10      #По умолчанию заголовок фрейма равен 10 байтам.
        self.version = version
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
        
    def GetFlags(self, music_file):
        currentPosition = music_file.tell()
        music_file.seek(self.startPosition+8)
        
        byte1 = music_file.read(1)              #Последовательное чтение двух байт флагов
        byte2 = music_file.read(1)
        bitFlags = ord(byte1)*256 + ord(byte2)  #Преобразование byte в int
        flags = {}
        
        if self.version == 3:
            for key in self.FLAG23_OFFSET:
                flags[key] = bitFlags>>self.FLAG23_OFFSET[key] & self.FIRST_BIT

        if self.version == 4:
            for key in self.FLAG24_OFFSET:
                flags[key] = bitFlags>>self.FLAG24_OFFSET[key] & self.FIRST_BIT
        
        music_file.seek(currentPosition)
        return flags
        
    def ReadHeader(self, music_file, startPosition):  
        self.startPosition = startPosition      
        self.id = self.GetId(music_file)
        self.dataLength = self.GetSize(music_file)
        self.flags = self.GetFlags(music_file)


class ID3Frame:
    """Основной объект ID3 тега
    
    Это базовый класс для различных видов тегов.
    """

    def __init__(self, id3Header):
        self.startPosition = 0
        self.id3Header = id3Header
        self.header = ID3FrameHeader(id3Header.version)
        self.data = 0
    
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
                raise NotImplementedError("Compression is not supported")
                
        elif self.id3Header.version == 3:
            if self.header.flags["COMPRESS"]:
                raise NotImplementedError("Compression is not supported")
            
            if self.header.flags["ENCRYPT"]:
                raise NotImplementedError("Encryption is not supported")

        music_file.seek(currentPosition)

        return data
    
    def ReadFrame(self, music_file, startPosition):
        self.startPosition = startPosition
        self.header.ReadHeader(music_file, startPosition)
        self.data = self.ReadData(music_file)

class ID3v2Tag:
    def __init__(self):
        self.header = ID3Header()
        self.tagList = {}
        
    def ReadTag(self, music_file):
        self.header.ReadHeader(music_file)
        
        position = 10
        while position < self.header.dataLength:
            frame = ID3Frame(self.header)
            frame.ReadFrame(music_file, position)
            
            if frame.header.id.decode() == "TIT1":   self.tagList["TIT1"] = TIT1(frame.data)
            elif frame.header.id.decode() == "TIT2": self.tagList["TIT2"] = TIT2(frame.data)
            elif frame.header.id.decode() == "TIT3": self.tagList["TIT3"] = TIT3(frame.data)
            elif frame.header.id.decode() == "TALB": self.tagList["TALB"] = TALB(frame.data)
            elif frame.header.id.decode() == "TRCK": self.tagList["TRCK"] = TRCK(frame.data)
            elif frame.header.id.decode() == "TPOS": self.tagList["TPOS"] = TPOS(frame.data)
            elif frame.header.id.decode() == "TSST": self.tagList["TSST"] = TSST(frame.data)
            elif frame.header.id.decode() == "TSRC": self.tagList["TSRC"] = TSRC(frame.data)
            elif frame.header.id.decode() == "TPE1": self.tagList["TPE1"] = TPE1(frame.data)
            else:
                self.tagList[frame.header.id.decode()] = frame
            position =position + frame.header.headerLength + frame.header.dataLength

class TextFrame:
    """Класс текстовых тегов.
    """
    def __init__(self, rawData):
        if isinstance(rawData, bytes):
            self.text = rawData.decode("UTF-8").strip("\x00")
        elif isinstance(rawData, str):
            self.text = rawData.strip("\x00")

class NumericTextFrame:
    """Класс числовых тегов.
    """
    def __init__(self,rawData):
        if isinstance(rawData, bytes):
            self.value = int(rawData.decode("UTF-8").strip("\x00"))
        elif isinstance(rawData, str):
            self.value = int(rawData.strip("\x00"))
        
class NumericPartTextFrame: 
    """ Класс тегов части последовательности напр. 5/14
    
        TODO: доделать правильное распознавание последовательности: 5/10
    """
    def __init__(self, rawData):
        self.value = rawData.decode("UTF-8").strip("")
    
class TIT1(TextFrame): "Принадлежность содержимого к группе"
class TIT2(TextFrame): "Название композиции"
class TIT3(TextFrame): "Подуровень названия композиции"
class TALB(TextFrame): "Название альбома"
class TOAL(TextFrame): "Оригинальное название композиции"
class TRCK(NumericTextFrame): "Номер дорожки"
class TPOS(NumericPartTextFrame): "Часть последовательности"
class TSST(TextFrame): "Название последовательности"
class TSRC(TextFrame): "International Standard Recording Code"
class TPE1(TextFrame): "Исполнитель"

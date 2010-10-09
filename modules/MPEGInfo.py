#coding=UTF-8

class MPEGHeaderNotFoundError(IOError): pass
class MPEGVersionError(IOError): pass
class MPEGLayerError(IOError): pass
class MPEGEmphasisError(IOError): pass
class MPEGBitrateError(IOError): pass

class MPEGInfo(object):
    """MPEG audio stream information"""
    
    def __init__ (self):
        ## 4 байта заголовка MPEG фрейма.
        self.byteHeader = 0
        ## Версия MPEG.
        self.MPEGVersion = 0
        ## Версия Layer.
        self.layer = 0
        ## Наличие биза защиты.
        self.protected = False
        ## Наличие бита смещения.
        self.padding = False
        ## Наличие бита приватности.
        self.private = False
        ## Наличие бита копирайта.
        self.copyright = False
        ## Наличие бита оригинала.
        self.original = False
        ## Значение акцента.
        self.emphasis = ""
        ## Битрейт (кбит/сек).
        self.bitRate = 0
        ## Частота дискретизации (Hz).
        self.sampleRate = 0
        ## Channel Mode.
        self.channelMode = ""
        ## Расширение Channel Mode.
        self.modeExtension = ""

    def CheckMarker (self):
        """ Осуществляется проверка правильности маркера фрейма.
            Проверяются первые 11 бит заголовка, если они содержат все единицы, то маркер не содержит ошибок и фрейм считается верным.
            Иначе генерируется исключение.
            
            @exception MPEGHeaderNotFoundError Если маркер фрейма содержит ошибку.
        """
        marker = (self.byteHeader[0]*256+self.byteHeader[1]) & 0xFFE0
        if marker != 0xFFE0:
            raise MPEGHeaderNotFoundError ("Wrong marker of the header")
            
    def GetMPEGVersion (self):
        """ Возвращает версию MPEG в видет строки. 
            
            @exception MPEGVersionError Если используется зарезервированное значение.
        """
        
        version = (self.byteHeader[1] & 0x18) >> 3     # 000xx000
        if version == 0:   return 2.5
        elif version == 1: raise MPEGVersionError("Wrong MPEG version")
        elif version == 2: return 2
        elif version == 3: return 1

    def GetLayerVersion (self):
        """ Возвращает версию Layer.             

            @exception MPEGLayerError Если используется зарезервированное значение.
        """

        layer = (self.byteHeader[1] & 0x06) >> 1      # 00000xx0
        if layer == 0:   raise MPEGLayerError("Wrong MPEG Layer index")
        elif layer == 1: return 3
        elif layer == 2: return 2
        elif layer == 3: return 1

    def GetProtectionBit (self):
        """ Возвращает наличие бита защиты (Protection Bit).
        
            @return True - если бит установлен в 1
            @return False - если бит установлен в 0
        """
        bit = self.byteHeader[1] & 0x01               # 0000000x
        if bit == 1: return False
        else: return True

    def GetBitrate (self):
        """ Возвращает битрейт. 
            Возвращаемое значение формируется из версии MPEG, версии Layer и считанного значения из заголовка фрейма.
            
            @exception MPEGBitrateError Если используется неверное значение для определения битрейта.
        """
        
        # (MPEGVersion, Layer)
        BITRATE = {
                    (1, 1):   [None, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, None],
                    (1, 2):   [None, 32, 48, 56,  64,  80,  96, 112, 128, 160, 192, 224, 256, 320, 384, None],
                    (1, 3):   [None, 32, 40, 48,  56,  64,  80,  96, 112, 128, 160, 192, 224, 256, 320, None],
                    (2, 1):   [None, 32, 48, 56,  64,  80,  96, 112, 128, 144, 160, 176, 192, 224, 256, None],
                    (2, 2):   [None,  8, 16, 24,  32,  40,  48,  56,  64,  80,  96, 112, 128, 144, 160, None],
                    (2, 3):   [None,  8, 16, 24,  32,  40,  48,  56,  64,  80,  96, 112, 128, 144, 160, None],
                    (2.5, 1): [None, 32, 48, 56,  64,  80,  96, 112, 128, 144, 160, 176, 192, 224, 256, None],
                    (2.5, 2): [None,  8, 16, 24,  32,  40,  48,  56,  64,  80,  96, 112, 128, 144, 160, None],
                    (2.5, 3): [None,  8, 16, 24,  32,  40,  48,  56,  64,  80,  96, 112, 128, 144, 160, None]
                  }
                   
        index = (self.byteHeader[2] & 0xF0) >> 4     # xxxx0000
        if index in [0, 15]:
            raise MPEGBitrateError("Wrong bitrate value")
            
        return BITRATE[(self.MPEGVersion, self.layer)][index]
        
    def GetSampleRate (self):
        """ Возвращает частоту дискретизации.
            Возвращаемое значение формируется из версии MPEG и считанного значения из заголовка фрейма.
        """
        RATES = {
                    1: [44100, 48000, 32000],
                    2: [22050, 24000, 16000],
                    2.5: [11025, 12000, 8000]
                }
        index = (self.byteHeader[2] & 0x0C) >> 2     # 0000xx00
        return RATES[self.MPEGVersion][index]
    
    def GetPaddingBit (self):
        """ Возвращает наличие бита смещения (Padding Bit).
            Если он установлен, то данные смещаются на 1 байт. Это важно для расчета размера фрейма.
            
            @return True - если бит установлен в 1
            @return False - если бит установлен в 0
        """
        bit = (self.byteHeader[2] & 0x02) >> 1         # 000000x0
        if bit == 1: return True
        else: return False
        
    def GetPrivateBit (self):
        """ Возвращает наличие часного бита (Private Bit).
            Используется только для информации.
            
            @return True - если бит установлен в 1
            @return False - если бит установлен в 0
        """        
        bit = self.byteHeader[2] & 0x01              # 0000000x
        if bit == 1: return True
        else: return False
        
    def GetChennelMode (self):
        """ Возвращает Channel Mode.
            
            @return Stereo, Join Stereo, Dual channel, Mono
        """        
        mode = (self.byteHeader[3] & 0xC0) >> 1      # xx000000
        if mode == 0: return "Stereo"
        elif mode == 1: return "Join Stereo"
        elif mode == 2: return "Dual channel"
        elif mode == 3: return "Mono"
        
    def GetModeExtension (self):
        """ Возвращает расширенный Channel Mode.
        
            @warning Not implemented yet.
        """
        pass

    def GetCopyrightBit (self):
        """ Возвращает наличие бита копирайта (Copyright Bit).
            Используется только для информации.
            
            @return True - если бит установлен в 1
            @return False - если бит установлен в 0
        """
        bit = (self.byteHeader[3] & 0x08) >> 3       # 0000x000
        if bit == 1: return True
        else: return False

    def GetOriginalBit (self):
        """ Возвращает наличие бита оригинала (Original Bit).
            Используется только для информации.
            
            @return True - если бит установлен в 1
            @return False - если бит установлен в 0
        """
        bit = (self.byteHeader[3] & 0x04) >> 2       # 00000x00
        if bit == 1: return True
        else: return False

    def GetEmphasis (self):
        """ Возвращает значение акцента (Emphasis).
            В данный момент практически не используется.
            
            @return None, 50/15 mc, CCIT J.17
            @exception MPEGEmphasisError Если используется зарезервированное значение поля
        """
        emphasis = self.byteHeader[3] & 0x03         # 000000xx
        if emphasis == 0: return "None"
        elif emphasis == 1: return "50/15 mc"
        elif emphasis == 2: raise MPEGEmphasisError("Using reserved value")
        elif emphasis == 3: return "CCIT J.17"

    def ReadInfo (self, music_file, offset):
        """ Читает и расшифровывает заголовок MPEG фрейма. 
        
            @param music_file Объект файла, открытого на чтение в режиме "r+b".
            @param offset Размер ID3v2 тега.
        """
        
        music_file.seek(offset+10)
        self.byteHeader = music_file.read(4)
        
        self.CheckMarker()
        
        self.MPEGVersion = self.GetMPEGVersion()
        self.layer = self.GetLayerVersion()
        self.protected = self.GetProtectionBit()
        self.padding = self.GetPaddingBit()
        self.private = self.GetPrivateBit()
        self.copyright = self.GetCopyrightBit()
        self.original = self.GetOriginalBit()
        self.emphasis = self.GetEmphasis()
        self.sampleRate = self.GetSampleRate()
        self.bitRate = self.GetBitrate()
        self.channelMode = self.GetChennelMode()

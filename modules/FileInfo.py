# -*- coding: UTF8 -*-

import os
import time

class FileInformation(object):
    """ Базованя информация о файле. """
    def __init__(self, path):
        if os.path.exists(path):
            ## Полный путь файла.
            self.fullPath = os.path.dirname(path) + "/" + os.path.basename(path)
            ## Путь к директории, где содержится файл.
            self.dirName = os.path.dirname(path)
            ## Имя файла.
            self.fileName = os.path.basename(path)
        else:
            raise IOError ('File does not exist: ' + path)
        
    def FileSize (self, humanize=None):
        """ Возвращает размер файла в указанных единицах.
            @param humanize Единицы, к которым приводится размер. Допустимые значения:'B', 'K', 'M', 'G', 'T' 
            @return Вещественное число - размер файла.
        """
        
        b=os.path.getsize(self.fullPath)
        if not humanize or humanize == "B": return b
        elif humanize == "K": return b/float(2**10)
        elif humanize == "M": return b/float(2**20)
        elif humanize == "G": return b/float(2**30)
        elif humanize == "T": return b/float(2**40)
        else: return None

    def MakeDictFromTime(self, timeStruct):
        """ Формирует словарь из структуры времени.
            
            @param timeStruct Структура времени.
            @return Словарь, свормированный из поданной на вход структуры времени.
        """
            
        DiffTime = {}
        DiffTime["Year"] = timeStruct.tm_year
        DiffTime["Month"] = timeStruct.tm_mon
        DiffTime["Day"] = timeStruct.tm_mday
        DiffTime["Hour"] = timeStruct.tm_hour
        DiffTime["Minute"] = timeStruct.tm_min
        DiffTime["Second"] = timeStruct.tm_sec
        DiffTime["DayOfWeek"] = timeStruct.tm_wday
        DiffTime["DayOfYear"] = timeStruct.tm_yday
        return DiffTime
        
    
    def FileAccessTime (self):
        """ Время последнего доступа к файлу.
            @return Словать с датой и временем последнего доступа к файлу.
        """
    
        return self.MakeDictFromTime(time.gmtime(os.path.getatime(self.fullPath)))
    
    def FileModificationTime (self):
        """ Время последнего изменения файла.
            @return Словать с датой и временем последнего изменения файла.
        """
    
        return self.MakeDictFromTime(time.gmtime(os.path.getmtime(self.fullPath)))


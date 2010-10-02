# -*- coding: UTF8 -*-

import os
import time

class FileInformation:
    def __init__(self, path):
        if os.path.exists(path):
            self.fullPath = os.path.dirname(path) + "/" + os.path.basename(path)
            self.dirName = os.path.dirname(path)
            self.fileName = os.path.basename(path)
        else:
            raise IOError ('File does not exist: ' + path)
        
    def FileSize (self, humanize=None):
        """ Функция возвращает размер файла в указанных единицах.
            Входные параметры: path - путь к файлу (строка)
                               humanize - единицы, к которым приводится размер 
                                          допустимые значения:'B', 'K', 'M', 'G', 'T' """
        
        b=os.path.getsize(self.fullPath)
        if not humanize or humanize == "B": return b
        elif humanize == "K": return b/float(2**10)
        elif humanize == "M": return b/float(2**20)
        elif humanize == "G": return b/float(2**30)
        elif humanize == "T": return b/float(2**40)
        else: return None

    def MakeDictFromTime(self, timeStruct):
        """ Функция возвращает словарь, свормированный из поданной на вход структуры времени.
            Входные параметры: timeStruct - структура времени. """
            
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
        """ Функция возвращает время(дату) последнего доступа к файлу.
            Входные параметры: path - путь к файлу (строка). """
    
        return self.MakeDictFromTime(time.gmtime(os.path.getatime(self.fullPath)))
    
    def FileModificationTime (self):
        """ Функция возвращает время(дату) последнего изменения файла.
            Входные параметры: path - путь к файлу (строка). """
    
        return self.MakeDictFromTime(time.gmtime(os.path.getmtime(self.fullPath)))


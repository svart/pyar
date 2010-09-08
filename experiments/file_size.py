# -*- coding: UTF8 -*-

import os
import time

def GetFileSizeByPath (path, humanize=None):
    """ Функция возвращает размер файла в указанных единицах.
        Входные параметры: path - путь к файлу (строка)
                           humanize - единицы, к которым приводится размер 
                                      допустимые значения:'B', 'K', 'M', 'G', 'T' """
        
    if os.path.exists(path):
        b=os.path.getsize(path)
        if not humanize or humanize == "B": return b
        elif humanize == "K": return b/float(2**10)
        elif humanize == "M": return b/float(2**20)
        elif humanize == "G": return b/float(2**30)
        elif humanize == "T": return b/float(2**40)
        else: return None
    else: return None

def MakeDictFromTime(timeStruct):
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
    

def GetFileAccessTime (path):
    """ Функция возвращает время(дату) последнего доступа к файлу.
        Входные параметры: path - путь к файлу (строка). """

    if os.path.exists(path):
        return MakeDictFromTime(time.gmtime(os.path.getatime(path)))

def GetFileModificationTime (path):
    """ Функция возвращает время(дату) последнего изменения файла.
        Входные параметры: path - путь к файлу (строка). """

    if os.path.exists(path):
        return MakeDictFromTime(time.gmtime(os.path.getmtime(path)))

#####################Testing##########################
        
print GetFileSizeByPath("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3", "M");
print GetFileAccessTime("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3")
print GetFileModificationTime("/media/FreeAgent/Music/Dark Age/2008 - Minus Exitus/01 - Minus Exitus.mp3")

#print GetFileSizeByPath.__doc__

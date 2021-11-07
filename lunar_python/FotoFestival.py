# -*- coding: utf-8 -*-


class FotoFestival:
    """
    佛历因果犯忌
    """

    def __init__(self, name, result=None, every_month=False, remark=None):
        self.__name = name
        self.__result = "" if result is None else result
        self.__everyMonth = every_month
        self.__remark = "" if remark is None else remark

    def getName(self):
        return self.__name

    def getResult(self):
        return self.__result

    def isEveryMonth(self):
        return self.__everyMonth

    def getRemark(self):
        return self.__remark

    def __str__(self):
        return self.toString()

    def toString(self):
        s = self.__name
        if self.__result is not None and len(self.__result) > 0:
            s += " " + self.__result
        if self.__remark is not None and len(self.__remark) > 0:
            s += " " + self.__remark
        return s

# -*- coding: utf-8 -*-


class TaoFestival:
    """
    道历节日
    """

    def __init__(self, name, remark=None):
        self.__name = name
        self.__remark = "" if remark is None else remark

    def getName(self):
        return self.__name

    def getRemark(self):
        return self.__remark

    def __str__(self):
        return self.toString()

    def toString(self):
        return self.__name

    def toFullString(self):
        s = self.__name
        if self.__remark is not None and len(self.__remark) > 0:
            s += "[" + self.__remark + "]"
        return s

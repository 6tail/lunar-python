# -*- coding: utf-8 -*-


class ShuJiu:
    """
    数九
    """

    def __init__(self, name, index):
        self.__name = name
        self.__index = index

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getIndex(self):
        return self.__index

    def setIndex(self, index):
        self.__index = index

    def __str__(self):
        return self.toString()

    def toString(self):
        return self.__name

    def toFullString(self):
        return "%s第%d天" % (self.__name, self.__index)

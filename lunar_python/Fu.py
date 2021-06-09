# -*- coding: utf-8 -*-


class Fu:
    """
    三伏
    <p>从夏至后第3个庚日算起，初伏为10天，中伏为10天或20天，末伏为10天。当夏至与立秋之间出现4个庚日时中伏为10天，出现5个庚日则为20天。</p>
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

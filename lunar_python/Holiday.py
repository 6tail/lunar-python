# -*- coding: utf-8 -*-
class Holiday:
    """
    节假日
    """

    def __init__(self, day, name, work, target):
        """
        初始化
        :param day: 日期，YYYY-MM-DD格式
        :param name: 名称，如：国庆
        :param work: 是否调休，即是否要上班
        :param target: 关联的节日，YYYY-MM-DD格式
        """
        self.__day = Holiday.__ymd(day)
        self.__name = name
        self.__work = work
        self.__target = Holiday.__ymd(target)

    @staticmethod
    def __ymd(s):
        return s if "-" in s else (s[0:4] + "-" + s[4:6] + "-" + s[6:])

    def getDay(self):
        return self.__day

    def getName(self):
        return self.__name

    def isWork(self):
        return self.__work

    def getTarget(self):
        return self.__target

    def setDay(self, day):
        self.__day = Holiday.__ymd(day)

    def setName(self, name):
        self.__name = name

    def setWork(self, work):
        self.__work = work

    def setTarget(self, target):
        self.__target = Holiday.__ymd(target)

    def toString(self):
        return "%s %s%s %s" % (self.__day, self.__name, "调休" if self.__work else "", self.__target)

    def __str__(self):
        return self.toString()

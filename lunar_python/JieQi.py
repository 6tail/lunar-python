# -*- coding: utf-8 -*-
from .util import LunarUtil


class JieQi:
    """
    节气
    """

    def __init__(self, name, solar):
        self.setName(name)
        self.__solar = solar

    def getName(self):
        """
        获取名称
        :return: 名称
        """
        return self.__name

    def setName(self, name):
        """
        设置名称
        :param name: 名称
        """
        self.__name = name
        for key in LunarUtil.JIE:
            if key == name:
                self.__jie = True
                return

        for key in LunarUtil.QI:
            if key == name:
                self.__qi = True
                return

    def getSolar(self):
        """
        获取阳历日期
        :return: 阳历日期
        """
        return self.__solar

    def setSolar(self, solar):
        """
        设置阳历日期
        :param solar: 阳历日期
        """
        self.__solar = solar

    def isJie(self):
        """
        是否节令
        :return: true/false
        """
        return self.__jie

    def isQi(self):
        """
        是否气令
        :return: true/false
        """
        return self.__qi

    def __str__(self):
        return self.__name
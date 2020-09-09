# -*- coding: utf-8 -*-


class JieQi:
    """
    节气
    """

    def __init__(self, name, solar):
        self.__name = name
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

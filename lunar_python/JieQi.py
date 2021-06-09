# -*- coding: utf-8 -*-


class JieQi:
    """
    节气
    """

    def __init__(self, name, solar):
        self.__name = name
        self.__jie = False
        self.__qi = False
        self.__solar = solar
        self.setName(name)

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
        from . import Lunar
        self.__name = name
        for i in range(0, len(Lunar.JIE_QI)):
            if name == Lunar.JIE_QI[i]:
                if i % 2 == 0:
                    self.__qi = True
                else:
                    self.__jie = True
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

    def toString(self):
        return self.__name

    def __str__(self):
        return self.toString()

# -*- coding: utf-8 -*-
from .util import LunarUtil


class NineStar:
    """
    九星
    """

    NUMBER = ("一", "二", "三", "四", "五", "六", "七", "八", "九")
    COLOR = ("白", "黒", "碧", "绿", "黄", "白", "赤", "白", "紫")
    WU_XING = ("水", "土", "木", "木", "土", "金", "金", "土", "火")
    POSITION = ("坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离")
    NAME_BEI_DOU = ("天枢", "天璇", "天玑", "天权", "玉衡", "开阳", "摇光", "洞明", "隐元")
    NAME_XUAN_KONG = ("贪狼", "巨门", "禄存", "文曲", "廉贞", "武曲", "破军", "左辅", "右弼")
    NAME_QI_MEN = ("天蓬", "天芮", "天冲", "天辅", "天禽", "天心", "天柱", "天任", "天英")
    BA_MEN_QI_MEN = ("休", "死", "伤", "杜", "", "开", "惊", "生", "景")
    NAME_TAI_YI = ("太乙", "摄提", "轩辕", "招摇", "天符", "青龙", "咸池", "太阴", "天乙")
    TYPE_TAI_YI = ("吉神", "凶神", "安神", "安神", "凶神", "吉神", "凶神", "吉神", "吉神")
    SONG_TAI_YI = ("门中太乙明，星官号贪狼，赌彩财喜旺，婚姻大吉昌，出入无阻挡，参谒见贤良，此行三五里，黑衣别阴阳。", "门前见摄提，百事必忧疑，相生犹自可，相克祸必临，死门并相会，老妇哭悲啼，求谋并吉事，尽皆不相宜，只可藏隐遁，若动伤身疾。", "出入会轩辕，凡事必缠牵，相生全不美，相克更忧煎，远行多不利，博彩尽输钱，九天玄女法，句句不虚言。", "招摇号木星，当之事莫行，相克行人阻，阴人口舌迎，梦寐多惊惧，屋响斧自鸣，阴阳消息理，万法弗违情。", "五鬼为天符，当门阴女谋，相克无好事，行路阻中途，走失难寻觅，道逢有尼姑，此星当门值，万事有灾除。", "神光跃青龙，财气喜重重，投入有酒食，赌彩最兴隆，更逢相生旺，休言克破凶，见贵安营寨，万事总吉同。", "吾将为咸池，当之尽不宜，出入多不利，相克有灾情，赌彩全输尽，求财空手回，仙人真妙语，愚人莫与知，动用虚惊退，反复逆风吹。", "坐临太阴星，百祸不相侵，求谋悉成就，知交有觅寻，回风归来路，恐有殃伏起，密语中记取，慎乎莫轻行。", "迎来天乙星，相逢百事兴，运用和合庆，茶酒喜相迎，求谋并嫁娶，好合有天成，祸福如神验，吉凶甚分明。")
    LUCK_XUAN_KONG = ("吉", "凶", "凶", "吉", "凶", "吉", "凶", "吉", "吉")
    LUCK_QI_MEN = ("大凶", "大凶", "小吉", "大吉", "大吉", "大吉", "小凶", "小吉", "小凶")
    YIN_YANG_QI_MEN = ("阳", "阴", "阳", "阳", "阳", "阴", "阴", "阳", "阴")

    def __init__(self, index):
        self.__index = index

    @staticmethod
    def fromIndex(index):
        return NineStar(index)

    def getNumber(self):
        return NineStar.NUMBER[self.__index]

    def getColor(self):
        return NineStar.COLOR[self.__index]

    def getWuXing(self):
        return NineStar.WU_XING[self.__index]

    def getPosition(self):
        return NineStar.POSITION[self.__index]

    def getPositionDesc(self):
        return LunarUtil.POSITION_DESC[self.getPosition()]

    def getNameInXuanKong(self):
        return NineStar.NAME_XUAN_KONG[self.__index]

    def getNameInBeiDou(self):
        return NineStar.NAME_BEI_DOU[self.__index]

    def getNameInQiMen(self):
        return NineStar.NAME_QI_MEN[self.__index]

    def getNameInTaiYi(self):
        return NineStar.NAME_TAI_YI[self.__index]

    def getLuckInQiMen(self):
        return NineStar.LUCK_QI_MEN[self.__index]

    def getLuckInXuanKong(self):
        return NineStar.LUCK_XUAN_KONG[self.__index]

    def getYinYangInQiMen(self):
        return NineStar.YIN_YANG_QI_MEN[self.__index]

    def getTypeInTaiYi(self):
        return NineStar.TYPE_TAI_YI[self.__index]

    def getBaMenInQiMen(self):
        return NineStar.BA_MEN_QI_MEN[self.__index]

    def getSongInTaiYi(self):
        return NineStar.SONG_TAI_YI[self.__index]

    def getIndex(self):
        return self.__index

    def __str__(self):
        return self.toString()

    def toString(self):
        return self.getNumber() + self.getColor() + self.getWuXing() + self.getNameInBeiDou()

    def toFullString(self):
        s = self.getNumber()
        s += self.getColor()
        s += self.getWuXing()
        s += " "
        s += self.getPosition()
        s += "("
        s += self.getPositionDesc()
        s += ") "
        s += self.getNameInBeiDou()
        s += " 玄空["
        s += self.getNameInXuanKong()
        s += " "
        s += self.getLuckInXuanKong()
        s += "] 奇门["
        s += self.getNameInQiMen()
        s += " "
        s += self.getLuckInQiMen()
        if len(self.getBaMenInQiMen()) > 0:
            s += " "
            s += self.getBaMenInQiMen()
            s += "门"
        s += " "
        s += self.getYinYangInQiMen()
        s += "] 太乙["
        s += self.getNameInTaiYi()
        s += " "
        s += self.getTypeInTaiYi()
        s += "]"
        return s
